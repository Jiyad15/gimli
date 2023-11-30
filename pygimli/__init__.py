# -*- coding: utf-8 -*-
"""
pyGIMLi - An open-source library for modelling and inversion in geophysics
"""
import sys
import locale

from .core.decorators import (renamed, singleton, moduleProperty,
                              skipOnDefaultTest, deprecate,
                              )

# Import everything that should be accessible through main namespace.
from .core import (BVector, CVector, DataContainer, DataContainerERT,
                   IVector, Line, Mesh, Plane, Pos, PosVector,
                   Vector, PosList, abs, cat, center, exp, find,
                   interpolate, log, log10, logDropTol, max,
                   mean, median, min, search, setThreadCount, sort,
                   Stopwatch, sum, trans, unique, versionStr, x, y, z, zero)

from .core import (isInt, isScalar, isIterable, isArray, isPos, 
                  isR3Array, isPosList, isVecField, isComplex, isMatrix)

from .core import math # alias all from .core.math.* to pg.math.*
# from .core import matrix # alias all from .core.matrix.* to pg.matrix.*
from .core.matrix import (BlockMatrix, Matrix, SparseMapMatrix, SparseMatrix)

from .core.logger import (_, _d, _g, _r, _y, _b, critical, d, debug,
                          deprecated, renameKwarg, renameArg,
                          error, info, debug, setDebug, setLogLevel, setVerbose, v,
                          verbose, warn)

warning = warn  # convenience

from .core.config import getConfigPath, rc, getCPUCount

from .meshtools import createGrid, interpolate
from .solver import solve
from .utils import boxprint, cache, cut, unique, unit, cmap, randn
from .utils import prettify as pf
from .utils.utils import Report, Table
def ppf(v): print(pf(v))

from .viewer import show, wait, noShow, hold

from .frameworks import fit
from .frameworks import Modelling
from .frameworks import Inversion
from .testing import test  #, setTestingMode, testingMode

from .math import matrix  # alias all from .core.matrix.* to pg.matrix.*
from .core.load import (load, optImport, getCachePath,
                        getExampleFile, getExampleData)



def checkAndFixLocaleDecimal_point(verbose=False):  # verbose overwritten
    """
    """
    if locale.localeconv()['decimal_point'] == ',':
        if verbose:
            print("Found locale decimal_point ',' "
                  "and change it to: decimal point '.'")
    try:
        locale.localeconv()['decimal_point']
        locale.setlocale(locale.LC_NUMERIC, 'C')
    except Exception as e:
        print(e)
        print('cannot set locale to decimal point')

    # LC_CTYPE should be something with UTF-8
    # export LC_CTYPE="de_DE.UTF-8"
    # python -c 'import sys; print(sys.stdout.encoding)'


checkAndFixLocaleDecimal_point(verbose=True)
# print(locale.localeconv()['decimal_point'])
# if locale.localeconv()['decimal_point'] == ',':
#   print("Found locale decimal_point ',' and change it to: decimal point '.'")
# try:
#    locale.localeconv()['decimal_point']
#    locale.setlocale(locale.LC_NUMERIC, 'C')
# except:
#    print('cannot set locale to decimal point')


if '--debug' in sys.argv or '-d' in sys.argv:
    setDebug(True)
else:
    setDebug(False)

if '--verbose' in sys.argv or '-v' in sys.argv:
    setVerbose(True)
else:
    setVerbose(False)

# if '--test' in sys.argv or '-t' in sys.argv:
#     setTestingMode(True)
# else:
#     setTestingMode(False)


###############################################################################
# Please leave this block here until the following issue is fixed:
# https://github.com/ContinuumIO/anaconda-issues/issues/1068
# if "conda" in __path__[0]:
#     try:
#         import PyQt5
#         import matplotlib
#         matplotlib.use("qt5agg", warn=False)
#     except ImportError:
#         pass
###############################################################################
__version__ = "0"


def findVersion(cache=True):  # careful: cache is already imported!
    """
    Find current version either generated by versioneer or from local cache
    to avoid extensive git systemcalls.
    """
    import os
    global __version__

    # setDebug(False)
    root = os.path.abspath(os.path.join(__file__, "../../"))
    gitPath = os.path.join(root, '.git')
    gitIndexFile = os.path.join(gitPath, 'index')
    versionCacheFile = os.path.join(getCachePath(), 'VERSION')
    versionPyFile = os.path.abspath(os.path.join(__file__, "_version.py"))

    loadCache = False

    if os.path.exists(versionCacheFile) and os.path.exists(gitIndexFile):
        # if git exists and cache is newer then load cache
        t1 = os.path.getmtime(versionCacheFile)
        t2 = os.path.getmtime(gitIndexFile)
        if t1 > t2:
            loadCache = True

    if os.path.exists(versionCacheFile) and os.path.exists(versionPyFile):
        # if git does not exists and cache is newer then _version.py load cache
        t1 = os.path.getmtime(versionCacheFile)
        t2 = os.path.getmtime(versionPyFile)
        if t1 > t2:
            loadCache = True

    if loadCache is True and cache is True:
        with open(versionCacheFile, 'r') as fi:
            __version__ = fi.read()
            debug('Loaded version info from cache.',
                  versionCacheFile, __version__)
        return __version__

    debug('Fetching version info.')
    from ._version import get_versions
    __versions__ = get_versions()
    __version__ = __versions__['version']

    def _get_branch():
        """Get current git branch."""
        from os.path import exists

        if exists(gitPath):
            from subprocess import check_output
            out = check_output(["git", "--git-dir", gitPath, "rev-parse",
                                "--abbrev-ref", "HEAD"]).decode("utf8")

            branch = out.split("\n")[0]
            if "HEAD" not in branch:
                return branch

        return None

    # def _get_latest_tag():
    #     from os.path import exists

    #     if exists(gitPath):
    #         from subprocess import check_output
    #         out = check_output(["git", "--git-dir", gitPath,
    #             "describe", "--tag"]).decode("utf8")

    #         tag = out.split("\n")[0].split('-')[0]
    #         return tag
    #     return None

    _branch = _get_branch()

    if __versions__["dirty"]:
        __version__ = __version__.replace(".dirty", " (with local changes")

        if _branch:
            __version__ += " on %s branch)" % _branch
        else:
            __version__ += ")"
    elif _branch and "+" in __version__:
        __version__ += " (%s)" % _branch

    if not os.path.exists(versionCacheFile):
        os.makedirs(os.path.dirname(versionCacheFile), exist_ok=True)

    with open(versionCacheFile, 'w') as fi:
        fi.write(__version__)
        debug('Wrote version info to cache:', versionCacheFile, __version__)

    return __version__


# call once to get version from cache, setup or _version.py
findVersion()


def version(cache=True):  # imported cach will be overwritten
    """Shortcut to show and return current version."""
    findVersion(cache=cache)
    if cache is True:
        info('Version (cached): ' + __version__ + " core:" + versionStr())
    else:
        info('Version: ' + __version__ + " core:" + versionStr())
    return __version__


def isNotebook():
    """Determine if run inside jupyther notebook or spyder"""
    import sys
    return 'ipykernel_launcher.py' in sys.argv[0]


@singleton
class SWatches(object):
    def __init__(self):
        self._sw = dict()
        
    def __getitem__(self, id):
        if not id in self._sw:
            self._sw[id] = Stopwatch(start=True)    
        
        return self._sw[id]

    def keys(self):
        return list(self._sw.keys())

    def items(self):
        return self._sw.items()

    def remove(self, key, isRoot=False):
        if isRoot is False:
            self._sw.pop(key, None)
        else:
            for k in list(self._sw.keys()):
                if k.startswith(key):
                    self._sw.pop(k, None)


def tic(msg=None, key=0):
    """Start global timer. Print elapsed time with `toc()`.

    You can start multiple stopwatches with optional identifier.

    Parameters
    ----------
    msg : string, optional
        Print message string just before starting the timer.
    key: identifier
        Identifier for your Stopwatch.
    """
    if msg:
        print(msg)
    
    SWatches()[key].start()


def toc(msg=None, box=False, stop=False, reset=False, key=0):
    """Print elapsed time since global timer was started with `tic()`.

    Arguments
    ---------
    msg: string [None]
        Print message string just after printing the elapsed time. If box is
        True, then embed msg into its own box
    box: bool [False]
        Embed the time in an ascii box
    stop: bool [False]
        Stops the stopwatch.
    reset: bool [False]
        Reset timer to 0.0 but don't stop it. Empties stored values.
    key: identifier
        Identifier for your Stopwatch.
    """
    if msg:
        if box is True:
            boxprint(msg)
        else:
            print(msg, end=' ')

    seconds = dur(key=key, stop=stop, reset=reset)

    ## refactor with prettyTime
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h <= 0 and m <= 0:
        time = pf(s)
    elif h <= 0:
        if m == 1.0:
            time = "%d minute and %.2f" % (m, s)
        else:
            time = "%d minutes and %.2f" % (m, s)
    elif h == 1.0:
        time = "%d hour, %d minutes and %.2f" % (h, m, s)
    else:
        time = "%d hours, %d minutes and %.2f" % (h, m, s)
    p = print if not box else boxprint

    if len(SWatches().keys()):
        p("Elapsed time ({0}) is {1} seconds.".format(key, time))
    else:
        p("Elapsed time is {0} seconds.".format(time))


def dur(key=0, stop=False, reset=False):
    """Return time in seconds since global timer was started with `tic()`.
    
    Arguments
    ---------
    key: identifier
        Identifier for your Stopwatch.
    stop: bool [False]
        Stops the stopwatch.
    reset: bool [False]
        Reset timer to 0.0 but don't stop it. Empties stored values.
    """
    if isinstance(stop, str):
        key = stop

    if stop is True:
        SWatches()[key].stop()
    return SWatches()[key].duration(restart=reset)
    

def store(key=0, stop=True):
    """Store current time in seconds since global timer was started with `tic()`.
    
    Arguments
    ---------
    stop: bool [True]
        Reset the stopwatch.
    key: identifier
        Identifier for your Stopwatch.
    """
    if stop is True:
        SWatches()[key].stop()
        
    return SWatches()[key].store()
    

class tictoc(object):
    """Timer class with persistant clock.
    """
    def __init__(self, key='', trace=None, reset=False):

        if reset is True:
            SWatches().remove(key, isRoot=True)

        if trace is not None:
            self._trace = trace
        else:
            self._trace = []

        if len(key) > 0:
            self._trace.append(key)
        self._key = '/'.join(self._trace)
        
        tic(key=self._key)

    def __call__(self, key):
        return tictoc(key, trace=self._trace)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        store(key=self._key)
        self._trace.pop()
                
    
class WithSkip(object):
    """ FallBack if you need empty with clause.
    """
    def __init__(self, *args, **kwargs):
        pass
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass


__MPL_PLT__ = None

def timings(name):
    """ Return table of timings for a given root swatch key name.
    """
    import numpy as np
    class TTree(object):
        def __init__(self, parent=None):
            self.parent = parent
            self.name = None
            self.childs = {}
            self.data = None
        
        def __getitem__(self, k):
            names = k.split('/')

            if self.name is None:
                self.name = names[0]
            else:
                if names[0] != self.name:
                    error(f'Wrong tree({self.name}) for {k}')
            
            if len(names) > 1:
                if names[1] not in self.childs:
                    self.childs[names[1]] = TTree(parent=self)
                
                return self.childs[names[1]]['/'.join(names[1:])]
                        
            return self

        @property
        def fullname(self):
            ps = self.name
            p = self.parent
            while 1:
                try:
                    ps = p.name + "/"+ ps
                    p = p.parent
                except:
                    break

            return ps + ":" + str(self.data)

        def __str__(self):
            s = self.fullname + "\n"
            for n, t in self.childs.items():
                s += str(t)

            return s

    tree = TTree()
    header = ['', 'single', 'count', 'sum', 'uncov.']
    table = []
    for k, s in SWatches().items():
        if isinstance(k, str):
            if k.startswith(name):

                ts = s.stored()
                # if len(ts) > 0:
                #     sts = sum(ts)
                table.append([k, np.mean(ts), len(ts), sum(ts), None])
                
                tree[k].data = sum(ts)
                
                # print(f'\t{k}: {pg.pf(sts)}s ({len(ts)} x {pg.pf(np.mean(ts)*1000)}ms)' )

    #print(tree)

    for t in table:
        if len(list(tree[t[0]].childs.keys())) > 0:
            
            t[-1] = t[-2]
            for n, tc in tree[t[0]].childs.items():
                try:
                    t[-1] -= tc.data 
                except:
                    pass

    #print(table)

    return Table(table, header)


# special shortcut pg.plt with lazy evaluation
__MPL_PLT__ = None

@moduleProperty
def _plt():
    #import time
    #t0 = time.time()
    global __MPL_PLT__, rc

    if __MPL_PLT__ is None:
        if rc['matplotlib'] is not None:
            try:
                get_ipython().run_line_magic('matplotlib', rc['matplotlib'])
                debug('matplotlib notebook backend set to: ', rc['matplotlib'])
            except NameError as e:
                pass
            except BaseException as e:
                info(f"matplotlib notebook backend set to {rc['matplotlib']} failed: ", e)
        # tic()        
        import matplotlib.pyplot as plt
        
        # if isNotebook():
        #     pass    
        # else:
        #     import matplotlib
        #     matplotlib.use('qtagg')
        #     print('############### importing plt took ', dur())
            
        #     print('############### backend:', plt.get_backend())

        from .viewer.mpl import registerShowPendingFigsAtExit, hold
        registerShowPendingFigsAtExit()

        # plt.subplots() resets locale setting to system default .. this went
        # horrible wrong for german 'decimal_point': ','
        # https://github.com/matplotlib/matplotlib/issues/6706
        # Qt5Agg resets it after importing figure;
        # TkAgg resets it after importing pyplot.
        # until its fixed we should maybe silently initialize the qt5agg backend &
        # refix the locale afterwards. If someone have a plan to do.

        checkAndFixLocaleDecimal_point(verbose=False)

        # Set global hold if mpl inline backend is used (as in Jupyter Notebooks)
        if 'inline' in plt.get_backend():
            hold(True)
        __MPL_PLT__ = plt

    return __MPL_PLT__
