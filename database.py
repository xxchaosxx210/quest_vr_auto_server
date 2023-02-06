from deta import Deta


PROJECT_KEY = "a098is8y_ahqJ4KZ1uawkftgZyEsRS3P9X8yKUDcg"

deta = Deta(PROJECT_KEY)

db = deta.Base("questVRAutoServerBase")

db.put({"name": "", "magnet": "", "version": 0.0, "filesize": 0})
