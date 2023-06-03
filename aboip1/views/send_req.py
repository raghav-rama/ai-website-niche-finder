import os
import pandas as pd
import sys
from aboip1.views.helper import list_files, cleanup
from aboip1.views.logging import getLogger
from aboip1.views.rate_limit_handling import completions_with_backoff
from tqdm import tqdm
from aboip1.views.inputs import Inputs

logger = getLogger()
result_dir = os.path.join(os.path.dirname(__file__), "results")

def get_gpt_response():
    batch_length = Inputs.batch_length
    from_row = Inputs.from_row
    to_row = Inputs.to_row
    FROM = Inputs.FROM
    TO = Inputs.TO
    logger.debug(f"from_row: {from_row}, to_row: {to_row}")
    logger.debug(f"from_row: {FROM}, to_row: {TO}")
    try:
        # TODO: remove this
        # flag = cleanup()
        flag = Inputs.flag
        pass
    except FileNotFoundError as e:
        print("File not found, make sure directory path is correctly is setup")
        logger.error("File not found, make sure directory path is correctly is setup")
    except Exception as e:
        print("Some error occured in cleanup")
        logger.exception("Exception: ")

    try:
        if not Inputs.df.empty:
            df = Inputs.df
        else:
            df = pd.read_csv(Inputs.input_csv, header=None)
    except FileNotFoundError:
        print("File not found, Re-upload and try again")
        logger.exception("Exception: ")
        sys.exit()
    except:
        print("Some error occured in reading file, Re-upload and try again")
        logger.exception("Exception: ")
        logger.debug(f"Inputs.input_csv in send_req.py: {Inputs.input_csv}")
        sys.exit()

    df_length = len(df.index)

    # TODO: remove 'or flag' from if condition
    # if Inputs.from_row == -1 or flag:
    if Inputs.from_row == -1:
        from_row, to_row = [0, df_length]
        FROM, TO = from_row, to_row

    try:
        website_names = df.iloc[from_row:to_row, 0]
        if len(website_names) < Inputs.batch_length:
            batch_length = len(website_names)
    except:
        print(f"Error reading input, running for all rows")
        logger.exception("Exception: ")
        website_names = df.iloc[:, 0]

    total_websites = len(website_names)

    results = []

    j = from_row

    if not Inputs.flag:
        try:
            with open(os.path.join(result_dir, "latest_j.txt"), "r") as f:
                j = int(f.read())
                from_row = j
                logger.debug(f"from_row: {from_row}")
        except FileNotFoundError:
            print("Running for the first time")
            logger.exception("Exception: ")
        except:
            print("Some error occured in reading j value, try again, starting from 0")
            logger.exception("Exception: ")

    try:
        logger.debug(f"inside try: from_row: {from_row}, to_row: {to_row}")
        logger.debug(f"inside try: from_row: {FROM}, to_row: {TO}")
        progress_bar = tqdm(
            range(from_row, to_row, batch_length), desc="Processing batches"
        )
        for i in progress_bar:
            website_batch = df.iloc[i : i + batch_length, 0]
            completion = completions_with_backoff(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"{Inputs.prompt_context}"},
                    {
                        "role": "user",
                        "content": f"{Inputs.prompt_question} {website_batch}",
                    },
                ],
                n=1,
                temperature=0.1,
                max_tokens=2048,
            )
            response = completion.choices[0].message.content
            logger.debug(f"response: {response}")
            websites_and_niches = response.split("\n")

            for website_and_niche in websites_and_niches:
                if not len(website_and_niche):
                    continue
                if website_and_niche.find(" - ") == -1:
                    continue
                website_and_niche_list = website_and_niche.split(" - ")
                try:
                    website = website_batch[j]
                except (KeyError, ValueError):
                    # print("f error: ", j, i)
                    logger.debug("f error: j, i = ", j, i)
                    j = i
                    logger.exception("Exception: ")
                    website = website_batch[j]
                # print("website: ", website)
                niches = website_and_niche_list[1]
                # print(website, niches)
                niche_list = niches.split(", ")
                # print(website, niche_list)
                result = [website, *niche_list]
                result_df = pd.DataFrame([result])
                result_df.to_csv(
                    os.path.join(
                        result_dir,
                        f"results-row{FROM}-row{TO}.csv",
                    ),
                    mode="a",
                    index=False,
                    header=False,
                )
                # results.append(result)
                with open(os.path.join(result_dir, "latest_j.txt"), "w") as f:
                    j += 1
                    # print("j: ", j)
                    f.write(str(j))
            # progress_bar.set_description(f"Total {i }")
    except Exception as e:
        with open(os.path.join(result_dir, "latest_j.txt"), "w") as f:
            f.write(str(j))
        print(
            "Some error occured, for more details, check logs, or, to resume re-run cell"
        )
        print("Error: ", type(e), e)
        logger.exception("Exception: ")
