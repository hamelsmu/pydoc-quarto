# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['get_modules', 'MarkdownDoc', 'render_quarto_md', 'gethelp', 'gen_md']

# %% ../nbs/00_core.ipynb 2
import pkgutil, re, inspect
from importlib import import_module
from pydoc import TextDoc, _isclass, resolve, describe
from types import ModuleType
from pathlib import Path
from fastcore.script import call_parse
from fastcore.xtras import mk_write

# %% ../nbs/00_core.ipynb 3
def get_modules(lib:ModuleType) -> list[str]:
    "get a list of modules from a python package"
    modules = []
    for _, modname, _ in pkgutil.iter_modules(lib.__path__, lib.__name__ + '.'):
        if not modname.split('.')[-1].startswith('_'): modules.append(modname)
    return modules

# %% ../nbs/00_core.ipynb 8
class MarkdownDoc(TextDoc):
    _skip_titles = ['file', 'data', 'version', 'author', 'credits', 'name']
    def _get_class_nm(text): return 

    def _bold_first_line(self, text):
        lines = text.splitlines()
        if lines: lines[0] = f'<strong>{lines[0].strip()}</strong>\n'
        return '\n'.join(lines)
    
    def title_format(self, text): return f'## {text.title()}\n'
    
    def bold(self, text): return text

    def indent(self, text, prefix='    '):
        """Indent text by prepending a given prefix to each line."""
        if not text: return ''
    
        lines = []
        for line in text.split('\n'):
            if not (line.strip().startswith('###') or line.strip().startswith('<strong>')):
                lines.append(prefix + line)
            else: 
                lines.append(line.strip())
                
        if lines: lines[-1] = lines[-1].rstrip()
        return '\n'.join(lines)

    
    def document(self, object, name=None, *args):
        """
        Generate documentation for an object.
        
        This method overrides pydoc.Doc.document in the standard library
        """
        args = (object, name) + args
        try:
            if inspect.ismodule(object): return self.docmodule(*args)
            elif _isclass(object): return f'\n### {name.strip()}\n\n' + self._bold_first_line(self.docclass(*args))
            elif inspect.ismethod(object) or '.' in object.__qualname__: return  f'\n#### `{object.__qualname__}`\n\n' + self.docroutine(*args)
            elif inspect.isroutine(object) and '.' not in object.__qualname__: return f'\n### `{name.strip()}`\n\n' + self._bold_first_line(self.docroutine(*args))
        except AttributeError:
            pass
        if inspect.isdatadescriptor(object): return self.docdata(*args)
        return self.docother(*args)

        
    def section(self, title, contents):
        if title.lower() in self._skip_titles: return ''
        clean_contents = self.indent(contents).rstrip()
        return self.title_format(title) + '\n' + clean_contents + '\n\n'

# %% ../nbs/00_core.ipynb 9
def render_quarto_md(thing, title=None, forceload=0):
    """Render text documentation, given an object or a path to an object."""
    renderer = MarkdownDoc()
    object, name = resolve(thing, forceload)
    desc = describe(object)
    module = inspect.getmodule(object)
    if name and '.' in name:
        desc += ' in ' + name[:name.rfind('.')]
    elif module and module is not object:
        desc += ' in module ' + module.__name__

    if not (inspect.ismodule(object) or
              _isclass(object) or
              inspect.isroutine(object) or
              inspect.isdatadescriptor(object) or
              _getdoc(object)):
        # If the passed object is a piece of data or an instance,
        # document its available methods instead of its value.
        if hasattr(object, '__origin__'):
            object = object.__origin__
        else:
            object = type(object)
            desc += ' object'
    
    doc_title = title if title else name
    desc_top = ' '.join(desc.splitlines()[:2])
    frontmatter=f'---\ntitle: "{doc_title}"\ndescription: "{desc_top}"\n---\n\n'
    return frontmatter + renderer.document(object, name)

# %% ../nbs/00_core.ipynb 10
def gethelp(modname:str, title:str=None)->str:
    "Get the help string for a module in a markdown format."
    sym = __import__(modname, fromlist=[''])
    return render_quarto_md(sym, title=title)

# %% ../nbs/00_core.ipynb 15
@call_parse
def gen_md(lib:str, # the name of the python library
           dest_dir:str # the destination directory the markdown files will be rendered into
          ) -> None:
    "Generate Quarto Markdown API docs"
    for modname in get_modules(import_module(lib)): 
        submod = modname.split('.')[-1]
        md = gethelp(modname=modname, title=submod)
        (Path(dest_dir)/f'{submod}.qmd').mk_write(md)
