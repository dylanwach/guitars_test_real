import craig
import schedule


craig.check_craig()
schedule.every(10).minutes.do(craig.check_craig)

while True:
    schedule.run_pending()