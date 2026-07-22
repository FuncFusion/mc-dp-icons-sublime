import os

for root, _, filenames in os.walk("./"):
	for fn in filenames:
		# print(fn)
		if "folder" in fn and "generic" not in fn and fn.endswith("png"):
			print(fn)
			os.remove("./"+fn)