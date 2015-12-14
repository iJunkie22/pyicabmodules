import plistlib
import base64
import io
import re


class ModuleConfig(object):
    def __init__(self, *args, **kwargs):
        self.icon1x = io.BytesIO()
        self.icon2x = io.BytesIO()
        self.module_dict = {'title': {}, 'description': {}}
        self.vars_array = []

    def add_description(self, conf_str):
        attr_name = conf_str.partition('=')[0]
        modifier = attr_name.partition('.')[2]
        if modifier is '':
            modifier = 'default'

        attr_val = conf_str.partition('=')[2]
        self.module_dict['description'][modifier] = attr_val

    def add_title(self, conf_str):
        attr_name = conf_str.partition('=')[0]
        modifier = attr_name.partition('.')[2]
        if modifier is '':
            modifier = 'default'

        attr_val = conf_str.partition('=')[2]
        self.module_dict['title'][modifier] = attr_val

    def add_icon(self, conf_str):
        if conf_str.startswith('icon2x'):
            self.icon2x.write(base64.b64decode(conf_str.partition('=')[2]))
        else:
            self.icon1x.write(base64.b64decode(conf_str.partition('=')[2]))

    def add_var(self, conf_str):
        v_parts = conf_str.rstrip(';').split(';')
        v_dict = {}
        for p in v_parts:
            p_n, sep, p_v = p.partition('=')
            v_dict[p_n] = p_v

        v_types = ('bool', 'int', 'string', 'pass', 'lang', 'confirm', 'autorun', 'select',
                   'boolean', 'integer', 'text', 'password', 'language', 'confirmation')
        v_type_int = v_types.index(v_dict['type']) % 8  # loose type string match

        assert 'var' in v_dict.keys()
        v_dict['name'] = v_dict.pop('var')
        v_dict['type'] = v_type_int
        if v_dict.get('default', None) in ('true', 'false'):
            v_dict['default'] = (v_dict['default'] == 'true')  # convert JS bool string to pyBool

        assert v_dict['type'] not in (0, 1, 2, 3, 7), 'These are not implemented yet!!'
        print "-->var", v_dict

        # TODO: Add support for bool, int, string, pass, and select


    @classmethod
    def from_string(cls, s2):
        new_module = cls()
        for line in s2.splitlines():
            if line.startswith('description'):
                new_module.add_description(line)
            elif line.startswith('title'):
                new_module.add_title(line)
            elif line.startswith('icon'):
                new_module.add_icon(line)
            elif line.startswith('var'):
                new_module.add_var(line)
        return new_module

    def __del__(self):
        self.icon1x.close()
        self.icon2x.close()

    def write_icons(self):
        i1 = open('icon1.png', 'wb')
        i2 = open('icon2.png', 'wb')
        i1.write(self.icon1x.getvalue())
        i2.write(self.icon2x.getvalue())
        i1.close()
        i2.close()


class Module(object):
    def __init__(self, header, contents):
        pass

    @classmethod
    def from_string(cls, s1):
        m_header = io.BytesIO()
        m_contents = io.BytesIO()

        capturing_header = False

        for line in s1.splitlines():
            # print line
            if line == "//startconfig":
                capturing_header = True

            elif capturing_header:
                if line == "//endconfig":
                    capturing_header = False
                else:
                    m_header.write(line[2:] + "\n")
            else:
                m_contents.write(line + "\n")

        print m_header.getvalue()
        mc1 = ModuleConfig.from_string(m_header.getvalue())
        m_header.close()
        print m_contents.getvalue()
        m_contents.close()
        mc1.write_icons()
        print mc1.module_dict


fd1 = open("690_Calculator-1.icabmodule", 'r')
flines = fd1.read()
fd1.close()

Module.from_string(flines)


