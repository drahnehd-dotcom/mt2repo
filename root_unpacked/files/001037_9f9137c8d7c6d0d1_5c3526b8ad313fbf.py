class Sandbox(object):
	WHITE_LIST = ['builtins', 'types', __name__, '__main__', 'sys']

	# Stara wersja na KAZDE ladowane okno robila copy.copy(sys.modules) (~1600 wpisow),
	# przechodzila po calej kopii zerujac niedozwolone moduly, a w finally odtwarzala caly
	# slownik - kilka tysiecy operacji na okno, ~84 okna na wejsciu do gry. Do tego petla
	# w finally kasowala klucze podczas iteracji po sys.modules (w Py3 = RuntimeError,
	# gdy skrypt cokolwiek doimportowal).
	# Teraz: podmieniamy __import__ tylko dla wykonywanego skryptu (koszt O(1) na import)
	# i zerujemy w sys.modules wylacznie krotka liste modulow, do ktorych skrypt moglby
	# siegnac przez sys.modules[...] (bo 'sys' jest na bialej liscie).
	BLOCKED_MODULES = (
		'os', 'os.path', 'ntpath', 'posixpath', 'subprocess', 'shutil', 'ctypes',
		'socket', 'pickle', 'marshal', 'importlib', 'tempfile', 'winreg',
	)

	# Bytecode layoutow nie zmienia sie w trakcie sesji - kompilujemy kazdy plik raz.
	_codeCache = {}

	def __init__(self, prevent_imported_modules = False, allowed_modules = [], prevented_modules = [], allowed_paths = []):
		self.prevent_imported_modules = prevent_imported_modules
		self.allowed_modules = allowed_modules
		self.prevented_modules = prevented_modules
		self.allowed_paths = allowed_paths

	def add_allowed_modules(self, allowed_modules):
		self.allowed_modules = self.allowed_modules + allowed_modules

	def add_prevented_modules(self, prevented_modules):
		self.prevented_modules = self.prevented_modules + prevented_modules

	def __MakeSandboxedBuiltins(self):
		import builtins

		realImport = builtins.__import__
		allowed = set(self.allowed_modules) | set(self.WHITE_LIST)
		prevented = set(self.prevented_modules)
		prevent = self.prevent_imported_modules

		def sandboxedImport(name, globalsDict = None, localsDict = None, fromlist = (), level = 0):
			rootName = name.split('.')[0]
			if rootName in prevented or (prevent and rootName not in allowed):
				raise ImportError("Sandbox: import of '%s' is not allowed here" % name)
			return realImport(name, globalsDict, localsDict, fromlist, level)

		sandboxed = dict(vars(builtins))
		sandboxed['__import__'] = sandboxedImport
		return sandboxed

	def __GetCode(self, filename):
		code = Sandbox._codeCache.get(filename)
		if code is not None:
			return code

		data = open(filename, 'rb').read()
		if isinstance(data, bytes):
			try:
				data = data.decode('utf-8')
			except UnicodeDecodeError:
				data = data.decode('latin-1')

		code = compile(data, filename, 'exec')
		Sandbox._codeCache[filename] = code
		return code

	def execfile(self, filename, dic):
		import sys

		for allowed_module_name in self.allowed_modules:
			try:
				__import__(allowed_module_name)
			except:
				sys.modules['dbg'].TraceError("UISCRIPT_LOAD_ERROR: Could not import %s [filename %s]" % (allowed_module_name, filename))

		blockedList = list(self.prevented_modules)
		if self.prevent_imported_modules:
			blockedList += [name for name in self.BLOCKED_MODULES if name not in self.allowed_modules]

		blockedBackup = {}
		for name in blockedList:
			blockedBackup[name] = sys.modules.get(name)
			sys.modules[name] = None

		dic['__builtins__'] = self.__MakeSandboxedBuiltins()

		try:
			exec(self.__GetCode(filename), dic)
		except Exception as e:
			sys.modules['dbg'].TraceError("UISCRIPT_LOAD_ERROR: %s [filename %s]" % (str(e), filename))
		finally:
			for name, module in blockedBackup.items():
				if module is None:
					sys.modules.pop(name, None)
				else:
					sys.modules[name] = module



def GetElementDictByName(dct, name):
	if 'children' in dct:
		for child in dct['children']:
			if 'name' in child:
				if child['name'] == name:
					return child

			if 'children' in child:
				search = GetElementDictByName(child, name)
				if search != None:
					return search
	return None
