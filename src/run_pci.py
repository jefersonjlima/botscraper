from botscraper import PCIContest
import logging

if __name__ == "__main__":

    etl = PCIContest()
    try:
        etl.run()
    except Exception as e:
        print(e)

