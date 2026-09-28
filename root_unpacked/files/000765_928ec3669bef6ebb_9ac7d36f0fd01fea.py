import sys
import app
import dbg

import builtins

import importlib
import importlib.util
import types
import marshal
import traceback as _traceback_mod
_chr		= builtins.chr
_ModuleType	= type(sys)

def debug(*args, **kwargs):
	try:
		import chat
		text = "{} " * (len(args) + len(kwargs))
		text = text[:-1]
		chat.AppendChat(chat.CHAT_TYPE_PARTY, text.format(*args, **kwargs))
	except Exception as err:
		pass

def debug_(*args, **kwargs):
	try:
		import dbg
		text = "{} " * (len(args) + len(kwargs))
		text = text[:-1]
		dbg.LogBox( text.format(*args, **kwargs) )
	except Exception as err:
		pass

builtins.debug = debug
builtins.msg   = debug_
sys.path = []
sys.path.append("lib")

class TraceFile:
	def __init__(self):
		self._inWrite = False
	def write(self, msg):
		dbg.Trace(msg)
		if self._inWrite:
			return
		if not isinstance(msg, str):
			return
		stripped = msg.strip()
		if not stripped:
			return
		if 'Error' not in stripped and 'Exception' not in stripped:
			return
		self._inWrite = True
		try:
			exc_type, exc_val, exc_tb = sys.exc_info()
			NL = chr(10)
			if exc_tb is not None:
				lines = _traceback_mod.format_exception(exc_type, exc_val, exc_tb)
				for line in lines:
					for sub in line.rstrip().split(NL):
						if sub.strip():
							dbg.TraceError('  STDOUT-TB: ' + sub)
			else:
				lines = _traceback_mod.format_stack(limit=20)
				for line in lines:
					for sub in line.rstrip().split(NL):
						if sub.strip():
							dbg.TraceError('  STDOUT-STACK: ' + sub)
		except Exception:
			pass
		finally:
			self._inWrite = False
	def flush(self):
		pass

class TraceErrorFile:
	def __init__(self):
		self._inWrite = False
	def write(self, msg):
		dbg.TraceError(msg)
		dbg.RegisterExceptionString(msg)
		if self._inWrite:
			return
		if not isinstance(msg, str):
			return
		stripped = msg.strip()
		if not stripped:
			return
		if 'Error' not in stripped and 'Exception' not in stripped:
			return
		self._inWrite = True
		try:
			exc_type, exc_val, exc_tb = sys.exc_info()
			NL = chr(10)
			if exc_tb is not None:
				lines = _traceback_mod.format_exception(exc_type, exc_val, exc_tb)
				for line in lines:
					for sub in line.rstrip().split(NL):
						if sub.strip():
							dbg.TraceError('  TB: ' + sub)
			else:
				lines = _traceback_mod.format_stack(limit=20)
				for line in lines:
					for sub in line.rstrip().split(NL):
						if sub.strip():
							dbg.TraceError('  STACK: ' + sub)
		except Exception:
			pass
		finally:
			self._inWrite = False
	def flush(self):
		pass

class LogBoxFile:
	def __init__(self):
		self.stderrSave = sys.stderr
		self.msg = ""

	def __del__(self):
		self.restore()

	def restore(self):
		sys.stderr = self.stderrSave

	def write(self, msg):
		self.msg = self.msg + msg

	def show(self):
		dbg.TraceError(self.msg)
		dbg.LogBox(self.msg,"Error")

sys.stdout = TraceFile()
sys.stderr = TraceErrorFile()

# Excepthook diagnostyczny - dump pelen traceback dla nieobsluzonych wyjatkow.
def _diagnosticExceptHook(exc_type, exc_val, exc_tb):
	try:
		NL = chr(10)
		dbg.TraceError('=== UNHANDLED EXCEPTION ===')
		lines = _traceback_mod.format_exception(exc_type, exc_val, exc_tb)
		for line in lines:
			for sub in line.rstrip().split(NL):
				if sub.strip():
					dbg.TraceError('  EXC: ' + sub)
		dbg.TraceError('=== END EXCEPTION ===')
	except Exception:
		pass
sys.excepthook = _diagnosticExceptHook

import marshal
import importlib
import importlib.util
import types
import pack
class pack_file_iterator(object):
	def __init__(self, packfile):
		self.pack_file = packfile

	def __iter__(self):
		return self

	def __next__(self):
		tmp = self.pack_file.readline()
		if tmp:
			return tmp
		raise StopIteration

_chr = __builtins__.chr

__builtins__.NEW_PACK_FILE = True
if NEW_PACK_FILE:
	__builtins__.old_len = len
class pack_file(object):
	def __init__(self, filename, mode = 'rb'):
		assert mode in ('r', 'rb')
		if not pack.Exist(filename):
			raise IOError('No file or directory'
)
		try:
			self.data = pack.Get(filename)
		except:
			self.data = b''
		if NEW_PACK_FILE and not self.data:
			tmp = old_open(filename)
			self.data = tmp and tmp.read() or b''
		if mode == 'r':
			if isinstance(self.data, bytes):
				try:
					self.data = self.data.decode('utf-8')
				except UnicodeDecodeError:
					self.data = self.data.decode('latin-1')
			self.data=_chr(10).join(self.data.split(_chr(13)+_chr(10)))
		if NEW_PACK_FILE:
			self.mode = mode
			self.closed = False
			self.tell_size = 0

	def __iter__(self):
		return pack_file_iterator(self)

	def read(self, length = 0):
		if not self.data:
			return ''
		if length:
			tmp = self.data[:length]
			if NEW_PACK_FILE:
				self.tell_size += old_len(tmp)
			self.data = self.data[length:]
			return tmp
		else:
			tmp = self.data
			if NEW_PACK_FILE:
				self.tell_size += old_len(tmp)
			self.data = ''
			return tmp

	def readline(self):
		return self.read(self.data.find(_chr(10))+1)

	def readlines(self):
		return [x for x in self]

	if NEW_PACK_FILE:
		def tell(self):
			return self.tell_size
		def close(self):
			self.closed = True
			self.data = ''
		def flush(self):
			pass
		def seek(self):
			pass

old_open = open
def open(filename, mode = 'rb'):
	if pack.Exist(filename) and mode in ('r', 'rb'):
		return pack_file(filename, mode)
	else:
		return old_open(filename, mode)

__builtins__.open = open
__builtins__.old_open = old_open
__builtins__.new_open = open

_ModuleType = type(sys)

old_import = __import__
def _process_result(code, fqname):
	is_module = isinstance(code, _ModuleType)

	if is_module:
		module = code
	else:
		module = types.ModuleType(fqname)


	sys.modules[fqname] = module

	if not is_module:
		exec(code, module.__dict__
)

	module = sys.modules[fqname]
	module.__name__ = fqname
	return module

module_do = lambda x:None
if __USE_CYTHON__:
	import rootlib

def __hybrid_import(name,globals=None,locals=None,fromlist=None, level=0):
	if level > 0:
		return old_import(name, globals, locals, fromlist, level)
	if __USE_CYTHON__ and rootlib.isExist(name):
		if name in sys.modules:
			dbg.Tracen('importing from sys.modules %s' % name)
			return sys.modules[name]

		dbg.Tracen('importing from rootlib %s' % name)
		newmodule = rootlib.moduleImport(name)

		module_do(newmodule)
		sys.modules[name] = newmodule
		return newmodule
	else:
		filename = name + '.py'

		if pack.Exist(filename):
			if name in sys.modules:
				dbg.Tracen('importing from sys.modules %s' % name)
				return sys.modules[name]

			dbg.Tracen('importing from pack %s' % name)

			data = pack_file(filename,'rb').read()
			try:
				data = data.decode('utf-8')
			except UnicodeDecodeError:
				data = data.decode('latin-1')
			newmodule = _process_result(compile(data,filename,'exec'),name)

			module_do(newmodule)
			return newmodule
		else:
			dbg.Tracen('importing from lib %s' % name)
			return old_import(name,globals,locals,fromlist,level)

def splitext(p):
	root, ext = '', ''
	for c in p:
		if c in ['/']:
			root, ext = root + ext + c, ''
		elif c == '.':
			if ext:
				root, ext = root + ext, c
			else:
				ext = c
		elif ext:
			ext = ext + c
		else:
			root = root + c
	return root, ext

def __IsCompiledFile__(sFileName):
	sBase, sExt = splitext(sFileName)
	sExt=sExt.lower()
	if sExt==".pyc" or sExt==".pyo":
		return 1
	else:
		return 0

def __LoadTextFile__(sFileName):
	sText=open(sFileName,'r').read()
	return compile(sText, sFileName, "exec")

def __LoadCompiledFile__(sFileName):
	kFile=open(sFileName)
	if kFile.read(4)!=importlib.util.MAGIC_NUMBER:
		raise

	kFile.read(4)

	kData=kFile.read()
	return marshal.loads(kData)

def execfile(fileName, dict):
	if __IsCompiledFile__(fileName):
		code=__LoadCompiledFile__(fileName)
	else:
		code=__LoadTextFile__(fileName)
	exec(code, dict)

import builtins
builtins.__import__ = __hybrid_import

builtins.old_execfile = execfile
builtins.execfile = execfile

def GetExceptionString(excTitle):
	(excType, excMsg, excTraceBack)=sys.exc_info()
	excText=""
	excText+=_chr(10)

	import traceback
	traceLineList=traceback.extract_tb(excTraceBack)

	for traceLine in traceLineList:
		if traceLine[0]=="<string>":
			excText+="%s(line:%d) " % (traceLine[2], traceLine[1])

	excText+=_chr(10)
	excText+=_chr(10)

	excText+=_chr(10)
	excText+="%s - %s:%s" % (excTitle, excType, excMsg)
	excText+=_chr(10)

	return excText

def ShowException(excTitle):
	excText=GetExceptionString(excTitle)
	dbg.TraceError(excText)
	return 0

def RunMainScript(name):
	try:
		execfile(name, __main__.__dict__)
	except RuntimeError as msg:
		msg = str(msg)

		import localeInfo
		if localeInfo.error:
			msg = localeInfo.error.get(msg, msg)

		dbg.TraceError(msg)
		dbg.LogBox(msg)
		pass

	except:
		import traceback
		msg = traceback.format_exc()
		dbg.TraceError(msg)
		dbg.LogBox(msg)
		pass

import debugInfo
debugInfo.SetDebugMode(__DEBUG__)

class DBG:
	STATE_SYS_ERR, STATE_CONSOLE, STATE_LOGBOX = range(0, 3)

	FUNC_ADRESS_DICT = {
		STATE_SYS_ERR : lambda arg : dbg.TraceError(arg),
		STATE_CONSOLE : lambda arg : dbg.Tracen(arg),
		STATE_LOGBOX : lambda arg : dbg.LogBox(arg),
	}

	@staticmethod
	def Execute(state, lines):
		""" A execute method which allow you to send unlimited arguments lines for debugging. """
		# If the state is console (Tracef), check if compiled executable is in debug-mode or not.
		isDebugMode = True if not __DEBUG__ else False
		if state == DBG.STATE_CONSOLE and not isDebugMode:
			return

		# If there's just one argument, convert it into a tuple.
		if not isinstance(lines, (tuple, list)):
			lines = tuple([lines])

		for line in lines:
			execute = DBG.FUNC_ADRESS_DICT.get(state, DBG.STATE_SYS_ERR)
			# By using custom string formatting it takes a format string and an arbitrary set of positional and keyword arguments.
			# Convert all data types into a specific string.
			execute('{}'.format(line))

builtins.TraceError = lambda *args : DBG.Execute(DBG.STATE_SYS_ERR, args)
builtins.Tracef = lambda *args : DBG.Execute(DBG.STATE_CONSOLE, args)
builtins.LogBox = lambda *args : DBG.Execute(DBG.STATE_LOGBOX, args)
builtins.sys_err = builtins.TraceError

loginMark = "-cs"

app.__COMMAND_LINE__ = __COMMAND_LINE__
if __USE_CYTHON__:
	import __main__
	__hybrid_import('Prototype', __main__.__dict__)
else:
	RunMainScript("prototype.py")
