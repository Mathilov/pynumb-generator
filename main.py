import random
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

start_time = time.time()
end_time = start_time + 5 * 60  # 5 minutes in seconds

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while time.time() < end_time:
        # generate and print a random number
        random_number = random.randint(1, 100)
        logging.info(f"Printing number {random_number}")

        # add a 5 second delay
        time.sleep(10)

    logging.info("Application finished")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
