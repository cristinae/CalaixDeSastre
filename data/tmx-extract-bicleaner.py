#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Dirty script to extract parallel sentences from Paracrawl/bicleaner with document
    separations
    The script has been modified from
    https://sourceforge.net/p/apertium/svn/49055/tree/trunk/apertium-awi/TmxTools/tmx-trim.py
    Date: 21.02.2019
    Author: cristinae
"""

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

import sys;

# encoding=utf8
reload(sys)
sys.setdefaultencoding('utf8')

class TMXHandler(ContentHandler):
	
	def __init__ (self, slang, tlang): 
		self.pair = set([slang, tlang]);
		self.inTag = '';
		#self.note = '';
		self.tuid = '';
		self.type = '';
		self.doc = '';
		self.docPrevious = 'buit';
		self.source = '';
		self.cur_pair = set();	
		self.cur_lang = '';
		self.seg = {};
		self.seg[slang] = '';
		self.seg[tlang] = '';
	

	def startElement(self, name, attrs): 

		if name == 'tu':  
			self.cur_pair = set();	
			self.inTag = 'tu';
			self.tuid = attrs.get('tuid','');
			self.type = attrs.get('datatype','');
		elif name == 'tuv': 
			self.inTag = 'tuv';
			self.cur_lang = attrs.get('xml:lang', '');
			self.cur_pair.add(self.cur_lang);
		elif name == 'seg': 
			self.inTag = 'seg';
			if self.cur_lang in self.pair: 
				self.seg[self.cur_lang] = '';
			#}
		elif name == 'prop': 
			self.inTag = 'prop';
			self.source = attrs.get('type','');
                        if self.source in 'source-document':
				self.doc = ''	

	def characters (self, c): 
		if self.inTag == 'note': 
			self.note += c;
		elif self.inTag == 'seg' and self.cur_lang in self.pair: 
			self.seg[self.cur_lang] += c;
		if self.inTag == 'prop':
			self.doc += c;

	def endElement(self, name): 
		if name == 'tu' and self.pair == self.cur_pair: 
                        if (self.docPrevious != self.doc.strip()):
			     print '\n';
			#print '<src>' + self.doc.strip();	
			#print '<src>' + self.docPrevious.strip();	
			for lang in self.cur_pair: 			
			     print '<'+lang+'> ' + self.seg[lang].strip();
		        self.docPrevious = self.doc.strip()


#	def endElement(self, name): #{
#		if name == 'tu' and self.pair == self.cur_pair: #{
#			print '  <tu tuid="' + self.tuid + '" datatype="' + self.type + '">';
#			print '    <note>' + self.note.strip() + '</note>';
#			for lang in self.cur_pair: #{			
#				print '    <tuv xml:lang="' + lang + '">';
#				print '      <seg>' + self.seg[lang].strip() + '</seg>';	
#				print '    </tuv>';
#			#}
#			print '  </tu>';
#		#}
#	#}
#}



parser = make_parser();

if len(sys.argv) < 3:
	print 'Usage: tmx-extract.py <file> <slang> <tlang>';
	print '';
	sys.exit(-1);

curHandler = TMXHandler(sys.argv[2], sys.argv[3]);

parser.setContentHandler(curHandler);

parser.parse(open(sys.argv[1]));



# DATA EXAMPLE
#   <tu tuid="421311448" datatype="Text">
#    <prop type="score">2.26538</prop>
#    <prop type="score-zipporah">2.7142</prop>
#    <prop type="score-bicleaner">0.7808</prop>
#    <prop type="lengthRatio">0.921052631579</prop>
#    <prop type="type">1:1</prop>
#    <tuv xml:lang="en">
#     <prop type="source-document">http://shop.wiltec.info/product_info.php/language/EN/tpl/clear/info/p5146_Bouton-d-arr-t-d-urgence-avec-LED-rouge-et-capuchon-rouge.html</prop>
#     <seg>! ! ! NOW with red STATUS LED ! ! !</seg>
#    </tuv>
#    <tuv xml:lang="de">
#     <prop type="source-document">http://shop.wiltec.info/product_info.php/language/EN/tpl/clear/info/p5146_Bouton-d-arr-t-d-urgence-avec-LED-rouge-et-capuchon-rouge.html</prop>
#     <seg>! ! ! JETZT mit roter STATUS LED ! ! !</seg>
#    </tuv>
#   </tu>

