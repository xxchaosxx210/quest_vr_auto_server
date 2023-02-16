from deta import Deta


PROJECT_KEY = "a098is8y_ahqJ4KZ1uawkftgZyEsRS3P9X8yKUDcg"

deta = Deta(PROJECT_KEY)

base_games = deta.Base("questVRAutoServerBase")

base_logs = deta.Base("questVRErrorLogs")
