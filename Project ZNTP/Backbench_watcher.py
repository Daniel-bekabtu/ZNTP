import os
import time
while True:
    with open("Exp_run_point", "r+") as watching_dog_point:
        point_of_watching_raw = watching_dog_point.readlines()
        print(point_of_watching_raw)
        point_of_watching_served = "".join(point_of_watching_raw)
        print(point_of_watching_served)
        if(point_of_watching_served == ""):
            print("ok. no-status")
        if(point_of_watching_served != ""):
            print("ok. status is detected, changing into execution point")
            execution_point_header = point_of_watching_served
            watching_dog_point.seek(0)
            watching_dog_point.truncate()
            os.system(f"py bin/zntp_web_server_{execution_point_header}.py")
        time.sleep(10)    