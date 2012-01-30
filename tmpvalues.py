#!/usr/bin/python -tt

def populate():
  dict = {}
  dict["en"] = {}
  dict["en"]['sadd'] = '<p class="note" id="sm01">If you are searching for this topic, add <strong>cowc:#%s</strong> to your search criteria.</p>'
  dict["en"]['smet'] = '<p class="note" id="sm13">The snippet for this category is: <strong>&lt;meta name="cowc" content="#%s" /&gt;</strong></p>'
  dict["en"]['shed'] = "<p class=\"note\" id=\"sm02\">You can add this snippet to your HTML's head section to enable search engines that use CCOW to categorize your site.</p>"
  dict["en"]["smul"] = '<p class="sugg" id="sm03">If the site/work covers multiple categories, its category might be '
  dict["en"]["scod"] = '</a>, and the code to designate it as such would be <strong>&lt;meta name="cowc" content="#%s" /&gt;</strong>.</p>'
  dict["en"]["snot"] = '<p class="drill" id="sm15">If this is not correct, choose a more specific category from the list below:</p>'
  dict["en"]["soop"] = "Top (start over)"
  dict["en"]["slan"] = "Change Language"
  dict["en"]["ssou"] = "\n\t<p class=\"source\" id=\"sm12\">You can obtain the source for this program at http://nowhere.yet</p>"
  dict["en"]["seng"] = "<p class=\"i18nerr\">\"%s\" could not be opened! Falling back to English. If you're seeing this in English, something is Impossible Bad Wrong.</p>"
  dict["en"]["snia"] = "<p class=\"wip\" id=\"gI1\">The information file \"%s\" could not be found/opened. Sorry.</p>"
  dict["en"]["sxpl"] = "Explanation of the Categories"
  dict["en"]['scc1'] = '\n\t<div class="cc" id="sm11">This helper application is released under a <a href="http://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-Share Alike</a> license.'
  dict["en"]['scc2'] = '\n\t<p>The contents of the translation and description files are released under a <a href="http://creativecommons.org/licenses/by-nd/3.0/">CC Attribution-No Derivative Works</a> license.</p> (C) copyright 2009-2012.</div>'
  dict["en"]["sms1"] = "One string (or more) is missing. Please contact the system administrator!"
  dict["en"]["xxxx"] = "Anything/Everything (root level)"
  dict["en"]["yxx0"] = "Multiplicity, the topic per se (Hol)"
  dict["en"]["yxx1"] = "Generaltiy, core principles of the topic (Ras)"
  dict["en"]["yxx2"] = "Mentality, Psychology, Philosophy of the topic (Dua)"
  dict["en"]["yxx3"] = "Communicability, Education, Transmission, Transportation (Chi)"
  dict["en"]["yxx4"] = "Sociality, Social aspects, Social impact (Ter)"
  dict["en"]["yxx5"] = "Provability, Empiricism, Objectivity, Realism, The recent past (Fum)"
  dict["en"]["yxx6"] = "Vitality, Life, Animals, Growth, Health, Medicine, Recreation, Leisure, The present (Sek)"
  dict["en"]["yxx7"] = "Sustainability, Provision, Agriculture, Plants, Horticulture, Maturity (Zab/Zabat)"
  dict["en"]["yxx8"] = "Spatiality, Community, Outer space, Locality (Med)"
  dict["en"]["yxx9"] = "Technology, Technical aspects (Neu)"
  dict["en"]["yxxa"] = "Memory, History, The distant past, Traditions (Uay)"
  dict["en"]["yxxb"] = "Artistry, The arts, Vision, The seen (Arz)"
  dict["en"]["yxxc"] = "Religion, Faith, The unseen, Rituality, Algorithm, Process, Procedure, Standards (Pax)"
  dict["en"]["yxxd"] = "Legality, The law, Government, Policy, Political science, Rules (Ord)"
  dict["en"]["yxxe"] = "Specificity, Individuality, Biography, Personal sites, Examples of the topic (Iyu)"
  dict["en"]["yxxf"] = "Marginality (Controversy, Conjecture, Unaccepted topics &c.), The future, Abnormalities (Ech)"
  dict["en"]["spro"] = "View Progress Report"
  return dict