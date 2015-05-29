import json
import browser
from global_holder import root
import browser
print=browser.console.log

def init():
	root.serialize_io_mapping={}
	print("serialize: Adding serialize_io_mapping")

class Serializable(object):
	def save(self):
		return {}

	def load(self, data):
		return self

class SimpleSerializable(Serializable):
	export_vars=[]

	def ss_export_hook_pre(self):
		pass

	def _export_vars(self, prefix=""):
		self.ss_export_hook_pre()
		temp={}
		for var in self.export_vars:
			if var in dir(self):
				temp[prefix+var]=save(getattr(self, var))
			else:
				browser.console.log("[WARNING] SimpleSerializable: "+str(self)+" did not have attr "+var+", although it was specified in it's export_vars (Ignored)")
		return temp

	def ss_import_hook_post(self):
		pass

	def _import_vars(self, data, prefix=""):
		for var in data:
			setattr(self, var, load(data[var], getattr(self, var) if var in dir(self) else None))
		self.ss_import_hook_post()

	def save(self):
		return self._export_vars()

	def load(self, data):
		self._import_vars(data)
		return self

def register_serializable(cls):
	root.serialize_io_mapping[cls.__name__]=cls
	return cls

def save_obj(obj):
	assert isinstance(obj, Serializable), "[ERROR] serialize.save_obj(obj): obj must be an instance of Serializable"
	assert obj.__class__ in root.serialize_io_mapping.values(), "[ERROR] serialize.save_obj(obj): obj must be registered with @register_serializable"
	data=obj.save()
	data["__class"]=[name for name in root.serialize_io_mapping.keys() if root.serialize_io_mapping[name]==obj.__class__][0]
	return data

def save(obj):
	if isinstance(obj, Serializable):
		return save_obj(obj)
	else:
		return obj

def load_obj(data, existing):
	assert "__class" in data, "[ERROR] serialize.load_obj(data): Malformed (missing __class)"
	assert data["__class"] in root.serialize_io_mapping, "[ERROR] serialize.load_obj(data): Invalid (__class not found)"
	if existing:
		assert existing.__class__.__name__==data["__class"], "[ERROR] serialize.load_obj(data, existing): Invalid exisitng (not same class)"
		return existing.load(data)
	else:
		return root.serialize_io_mapping[data["__class"]]().load(data)

def load(data, existing=None):
	if "__class" in data:
		return load_obj(data, existing)
	else:
		return data