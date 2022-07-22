# Default ESSID is CenturyLinkXXXX
# Zyxel C1000Z, C1100Z, C2100Z and C3100Z
import hashlib
import argparse

def centurylink(serial):

	junk = 'agnahaakeaksalmaltalvandanearmaskaspattbagbakbiebilbitblableblib'\
	'lyboabodbokbolbomborbrabrobrubudbuedaldamdegderdetdindisdraduedu'\
	'kdundypeggeieeikelgelvemueneengennertesseteettfeifemfilfinflofly'\
	'forfotfrafrifusfyrgengirglagregrogrygulhaihamhanhavheihelherhith'\
	'ivhoshovhuehukhunhushvaideildileinnionisejagjegjetjodjusjuvkaika'\
	'mkankarkleklikloknaknekokkorkrokrykulkunkurladlaglamlavletlimlin'\
	'livlomloslovluelunlurlutlydlynlyrlysmaimalmatmedmegmelmenmermilm'\
	'inmotmurmyemykmyrnamnednesnoknyenysoboobsoddodeoppordormoseospos'\
	'sostovnpaiparpekpenpepperpippopradrakramrarrasremrenrevrikrimrir'\
	'risrivromroprorrosrovrursagsaksalsausegseiselsensessilsinsivsjus'\
	'jyskiskoskysmisnesnusolsomsotspastistosumsussydsylsynsyvtaktalta'\
	'mtautidtietiltjatogtomtretuetunturukeullulvungurourtutevarvedveg'\
	'veivelvevvidvikvisvriyreyte'

	serial = serial.lower()
	search = serial.find("s")
	if search > 0 and serial[0:3] != "c11":
		serial = serial[search:]

	md5 = hashlib.md5()
	md5.update(serial.encode())

	p = ""
	summ = 0
	for b in md5.digest():
		d1 = hex(b)[2:].upper()
		if len(d1) == 1:
			d1 += d1
		p += d1
	summ = sum([ord(char) for char in p])
	i = summ % 265
	if summ & 1:
		s1 = hex(ord(junk[1 + i * 3 - 1]))[2:]
		s1 += hex(ord(junk[2 + i * 3 - 1]))[2:]
		s1 += hex(ord(junk[3 + i * 3 - 1]))[2:]
	else:
		s1 = hex(ord(junk[1 + i * 3 - 1]))[2:].upper()
		s1 += hex(ord(junk[2 + i * 3 - 1]))[2:].upper()
		s1 += hex(ord(junk[3 + i * 3 - 1]))[2:].upper()

	s2 = "%s%s%s%s%s%s%s%s%s%s" % (p[6:32], p[2], s1[0:2], p[5], p[2], s1[2:4], p[4], p[1], p[0], s1[4:6])

	md52 = hashlib.md5()
	md52.update(s2.encode())
	hex_digest = ""
	for b in md52.digest():
		d2 = hex(b)[2:].upper()
		if len(d2) == 1:
			d2 += d2
		hex_digest += d2
	p2 = hex_digest

	filler = "AD3EHKL6V5XY9PQRSTUGN2CJW4FM7ZL"
	bad_chars = "01259"

	key = hex_digest[12:26][::-1].lower()
	ascii_p2 = [ord(char) for char in p2]

	if key[0] in bad_chars:
		shift1 = 0
		shift2 = 1
		shift3 = 2
		value1 = ascii_p2[8]
		value2 = ascii_p2[0] >> shift2
		value3 = ascii_p2[2] >> shift3
		ascii_sum = value1+value2+value3
		replacement = filler[ascii_sum % 31]
		key = replacement.lower() + key[1:]

	for i in range(0, 14):
		if key[i] in bad_chars:
			shift1 = i % 4
			shift2 = i % 5
			shift3 = 3
			value1 = ascii_p2[i-1] >> shift1
			value2 = ascii_p2[i] >> shift2
			value3 = ascii_p2[i+1] >> shift3
			ascii_sum = value1 + value2 + value3
			replacement = filler[ascii_sum % 31]
			key = "%s%s%s" % (key[:i], replacement.lower(), key[i+1:])

	bad_output = "01259IJOQSZgijloqsz"
	output_replacements = "3B7C864EAFD"

	for pos in range(0, 14):
		for bad_pos in range(0, 19):
			if bad_output[bad_pos] == key[pos]:
				add = pos + 8
				key = "%s%s%s" % (key[:pos], output_replacements[add % 11].lower(), key[pos+1:])
	print(key)


parser = argparse.ArgumentParser(description='Centurylink keygen')
parser.add_argument('serial', help='Serial Number')
args = parser.parse_args()

centurylink(args.serial)
