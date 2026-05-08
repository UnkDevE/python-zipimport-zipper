import importlib.metadata
import importlib
import zipfile
import os
import sys


# @path should be the path to main point of entry in your module
# @fname is the file name for output
def compress_packages(fname, path):
    PATH = str(os.path.dirname(os.path.realpath(path)))
    dists = importlib.metadata.packages_distributions()

    if os.path.isfile("{}.zip".format(fname)):
        os.remove("{}.zip".format(fname))

    zf = zipfile.ZipFile("{}.zip".format(fname), "w")
    for k in dists.keys():
        module = None
        try:
            module = importlib.import_module(k)
        except ModuleNotFoundError:
            pass
        finally:
            if module is not None:
                directory = os.path.relpath(os.path.dirname(module.__file__),
                                            start=PATH)
                print(directory)
                for dirname, subdirs, files in os.walk(directory):
                    rdir = os.path.relpath(dirname, start=directory)
                    zf.write(directory, arcname=rdir)
                    for filename in files:
                        zf.write(os.path.join(dirname, filename),
                                 arcname=os.path.join(rdir, filename))
                    else:
                        pass

    zf.close()


if __name__ == '__main__':
    # find virutalenv and replicate site-packages in zipped folder
    # if not global install
    if sys.prefix != "/usr":
        compress_packages("site-packages", sys.prefix)
