#!/usr/bin/python -tt

def populate():
  dict = {}
  dict["0xxx"] = 'Multiplicity, Collections, Search Engines, etc.'
  dict["00xx"] = 'Portals and Aggregators'
  dict["000x"] = 'Search Engines and Directories'
  dict["0000"] = 'Metasearch Search Engines'
  dict['1xxx'] = 'General Knowledge and Systems'
  dict['2xxx'] = 'Psychology and Philosophy'
  dict['3xxx'] = 'Communications'
  dict['4xxx'] = 'Social Sciences'
  dict['5xxx'] = 'Hard Sciences'
  dict['6xxx'] = 'Medicinal Sciences, Recreation'
  dict['7xxx'] = 'Agriculture, Horticulture, etc.'
  dict['8xxx'] = 'Geography'
  dict['9xxx'] = 'Technology'
  dict['axxx'] = 'History'
  dict['bxxx'] = 'The Arts'
  dict['cxxx'] = 'Religion and Faith'
  dict['dxxx'] = 'Law, Government, etc.'
  dict['exxx'] = 'Biography, Personal sites/works, Names &amp; Insignia, Genealogy'
  dict['fxxx'] = 'Fiction'
  dict['03xx'] = 'Periodicals'
  dict['04xx'] = 'Organizations and Associations'
  dict['05xx'] = 'Bibliographies'
  dict['0axx'] = 'Archives'
  dict['0bxx'] = 'Collections, Collecting'
  dict['0cxx'] = 'News'
  dict['0fxx'] = 'Print-specific Items'
  dict['10xx'] = 'Library and Information Science'
  dict['11xx'] = 'Encyclopedias, Factbooks'
  dict['12xx'] = 'Systems'
  dict['14xx'] = 'Quotations'
  dict['19xx'] = 'Data Processing, Computer Science, Programming, and Programs'
  dict['1axx'] = 'Museum Science'
  dict['sadd'] = '<p class="note" id="sm01">If you are searching for this topic, add <strong>cowc:#%s</strong> to your search criteria.</p>'
  dict['smet'] = '<p class="note" id="sm13">The snippet for this category is: <strong>&lt;meta name="cowc" content="#%s" /&gt;</strong></p>'
  dict['shed'] = "<p class=\"note\" id=\"sm02\">You can add this snippet to your HTML's head section to enable search engines that use CCOW to categorize your site.</p>"
  dict["smul"] = '<p class="sugg" id="sm03">If the site/work covers multiple categories, its category might be '
  dict["scod"] = '</a>, and the code to designate it as such would be <strong>&lt;meta name="cowc" content="#%s" /&gt;</strong>.</p>'
  dict["snot"] = '<p class="drill" id="sm15">If this is not correct, choose a more specific category from the list below:</p>'
  dict["soop"] = "Top (start over)"
  dict["slan"] = "Change Language"
  dict["ssou"] = "\n\t<p class=\"source\" id=\"sm12\">You can obtain the source for this program at http://nowhere.yet</p>"
  dict["seng"] = "<p class=\"i18nerr\">\"%s\" could not be opened! Falling back to English. If you're seeing this in English, something is Impossible Bad Wrong.</p>"
  dict["snia"] = "<p class=\"wip\" id=\"gI1\">The information file \"%s\" could not be found/opened. Sorry.</p>"
  dict["sxpl"] = "Explanation of the Categories"
  dict['scc1'] = '\n\t<div class="cc" id="sm11">This helper application is released under a <a href="http://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-Share Alike</a> license.'
  dict['scc2'] = '\n\t<p>The contents of the translation and description files are released under a <a href="http://creativecommons.org/licenses/by-nd/3.0/">CC Attribution-No Derivative Works</a> license.</p> (C) copyright 2009-2012.</div>'
  dict["sms1"] = "One string (or more) is missing. Please contact the system administrator!"
  dict["xxxx"] = "Anything/Everything (root level)"
  dict["yxx0"] = "Multiplicity, the topic per se (Hol)"
  dict["yxx1"] = "Generaltiy, core principles of the topic (Ras)"
  dict["yxx2"] = "Mentality, Psychology, Philosophy of the topic (Dua)"
  dict["yxx3"] = "Communicability, Education, Transmission, Transportation (Chi)"
  dict["yxx4"] = "Sociality, Social aspects, Social impact (Ter)"
  dict["yxx5"] = "Provability, Empiricism, Objectivity, Realism, The recent past (Fum)"
  dict["yxx6"] = "Vitality, Life, Animals, Growth, Health, Medicine, Recreation, Leisure, The present (Sek)"
  dict["yxx7"] = "Sustainability, Provision, Agriculture, Plants, Horticulture, Maturity (Zab/Zabat)"
  dict["yxx8"] = "Spatiality, Community, Outer space, Locality (Med)"
  dict["yxx9"] = "Technology, Technical aspects (Neu)"
  dict["yxxa"] = "Memory, History, The distant past, Traditions (Uay)"
  dict["yxxb"] = "Artistry, The arts, Vision, The seen (Arz)"
  dict["yxxc"] = "Religion, Faith, The unseen, Rituality, Algorithm, Process, Procedure, Standards (Pax)"
  dict["yxxd"] = "Legality, The law, Government, Policy, Political science, Rules (Ord)"
  dict["yxxe"] = "Specificity, Individuality, Biography, Personal sites, Examples of the topic (Iyu)"
  dict["yxxf"] = "Marginality (Controversy, Conjecture, Unaccepted topics &amp;c.), The future, Abnormalities (Ech)"

  return dict