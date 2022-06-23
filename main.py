from tkinter import *
import threading, time
import math, random, re
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog

# Possible errors
COULD_NOT_FIND_FAVICON_ERROR_TITLE = 'Favicon not found'
COULD_NOT_FIND_FAVICON_ERROR_MESSAGE = 'Could not find the lock_icon.png file\nexiting program...'
COULD_NOT_FIND_QUADGRAM_FILE_TITLE = 'Quadgram file not found'
COULD_NOT_FIND_QUADGRAM_FILE_MESSAGE = 'Could not find the english_quadgrams.txt file\nwould you like to search the file manually?'

root = Tk()
root.title('Substitution Cipher - Quadgram Statistics')
root.resizable(False, False)
root.geometry('750x450')
root.configure(bg='#79a0e8')

try:
	photo = PhotoImage(file = "lock_icon.png")
	root.iconphoto(False, photo)
except:
	print(COULD_NOT_FIND_FAVICON_ERROR_MESSAGE)
	tkinter.messagebox.showerror(title=COULD_NOT_FIND_FAVICON_ERROR_TITLE, message=COULD_NOT_FIND_FAVICON_ERROR_MESSAGE)
	root.destroy()

def decrypt_encrypted_text():
	# we cant just print the decrypted text, because we wat to
	# print the spaces as well, at the right indexes
	def PrintDecryptedText(plaintext, spaces_indexes):
		plaintext_spaces = ''
		for letter_index in range(len(plaintext)):
			if(letter_index in spaces_indexes):
				print(' ', end='')
				plaintext_spaces += ' '
			print(plaintext[letter_index], end='')
			plaintext_spaces += plaintext[letter_index]
		return plaintext_spaces

	# before we are removing the spaces on the text, we want to save the indexes of those
	spaces_indexes = []

	# getting the encrypted text from a file called encrypted_text.txt
	# encrypted_text_file = open('encrypted_text.txt', encoding="utf8")
	encrypted_text_file = input_field.get("1.0",'end-1c')
	print(encrypted_text_file)
	# gross_encrypted_text = encrypted_text_file.read().upper().replace('\n', ' ')
	gross_encrypted_text = encrypted_text_file.upper().replace('\n', ' ')
	gross_encrypted_text = re.sub(r'[^A-Z ]', '', gross_encrypted_text)

	# now, we are iterating over the letters.
	# if the letter is space, save that location
	# if the letter is a capital letter, add that to the encrypted_text
	encrypted_text = ''
	for letter_index in range(len(gross_encrypted_text)):
		if(gross_encrypted_text[letter_index] == ' '):
			spaces_indexes.append(letter_index-len(spaces_indexes))
		elif('A' <= gross_encrypted_text[letter_index] <= 'Z'):
			encrypted_text += gross_encrypted_text[letter_index]
	# encrypted_text_file.close()

	# getting the quadgrams from the file called english_quadgrams
	quadgramsFile = 0
	try:
		quadgramsFile = open('english_quadgrams.txt', encoding="utf8")
	except:
		print(COULD_NOT_FIND_QUADGRAM_FILE_MESSAGE)
		user_answer = tkinter.messagebox.askyesno(title=COULD_NOT_FIND_FAVICON_ERROR_TITLE, message=COULD_NOT_FIND_QUADGRAM_FILE_MESSAGE)
		print(user_answer)
		if(user_answer == True):
			file_name = filedialog.askopenfilenames(title='Open files', initialdir='/', filetypes=(('text files', '*.txt'),))
			try:
				quadgramsFile = open(file_name[0], encoding="utf8")
			except:
				print('Cannot open the selected file\nexiting program...')
		else:
			root.destroy()

	quadgramsEnglish = quadgramsFile.readlines()
	quadgramsFile.close()

	# We would like to orgenize the data of the quadgrams in dictionary
	quadgramsDictionary = {}
	# Now, we would like to fill up the dictionary
	for quadgram in quadgramsEnglish:
		quadgramsDictionary[quadgram.split(' ')[0]] = int(quadgram.split(' ')[1][:-1])
	totalQuadgrams = sum(quadgramsDictionary.values())

	# We would like to start off from something, so will be generating random cipherKey
	# and we'll be replacing better options with better quadgrams
	abc_list = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
	random.shuffle(abc_list)
	cipherKey = ''.join(abc_list) # this is the cipherKey start point
	# from now, it will be replaced with better options...

	best_fitness = 0
	bestCipherKey = cipherKey # we will start using that key

	# now, will calcualte the worst similiar_to_english case, so will replace that for sure
	for index in range(len(encrypted_text) - 3): # -3 because we are iterating every 4 chars everytime
		probability = 0.1 / totalQuadgrams # 0.1 is the least possibility in the english quadgrams text file (which is also %1)
		logProbability = math.log(probability) # why are we using log, in the word file
		best_fitness += logProbability

	counter = 0
	while counter < 1000 and currnet_working_to_find_current_key==True:
		plaintext = ''

		# now, we are going to decrypt according to the current cipherKey
		# and after that we'll be analying that decrypted text, if the similarity to english is better
		# we are going to replace the alphabet to that...
		for character in encrypted_text:
			plaintext += chr(cipherKey.index(character) + ord('a'))

		# now we are going to calculate the fitness of the current alphabet
		# if it will be better, we are going to replace the best alphabet
		# to the current alphabet and repeat that proccess.
		fitness_current_alphabet = 0
		for index in range(len(plaintext) - 3): # -3 because we are iterating every 4 chars
			# now, we are looking at 4 chars at a time, which also called quadgram.
			# if the quadgram is not on the list, we are going to put the least probability which is 0.1
			# if the quadgram is in the list, we are going to calculate the probability
			current_quadgram = plaintext[index : index + 4].upper()
			if current_quadgram in quadgramsDictionary:
				probability = quadgramsDictionary[current_quadgram]/totalQuadgrams
			else:
				probability = 0.1 / totalQuadgrams

			# as we did before, we are going to parse that to log
			logProbability = math.log(probability)
			fitness_current_alphabet += logProbability

		if fitness_current_alphabet > best_fitness:
			best_fitness = fitness_current_alphabet
			bestCipherKey = cipherKey
			counter = 0
			# print('Current best plaintext is %s with key %s' % (plaintext, cipherKey))
			print('Current best plaintext is: ', end='')
			plaintext_spaces = PrintDecryptedText(plaintext, spaces_indexes)
			print()
			color = f'{"#%06x" % random.randint(0, 0xFFFFFF)}'
			current_key.config(text='Current cipherkey: {}'.format(cipherKey), fg=color)
			decrypted_field.delete(1.0, tk.END)
			decrypted_field.insert("end-1c", plaintext_spaces)
			time.sleep(0.005)

		# if we haven't improve our fitness with that alphabet,
		# just return to the best alphabet and try again...
		cipherKey = bestCipherKey

		character1Index = random.randint(0, 25)
		character2Index = random.randint(0, 25)
		temp = cipherKey[character1Index]
		cipherKey = cipherKey[: character1Index] + cipherKey[character2Index] + cipherKey[character1Index + 1 :]
		cipherKey = cipherKey[: character2Index] + temp + cipherKey[character2Index + 1 :]

currnet_working_to_find_current_key = False

def mid( ):
	global currnet_working_to_find_current_key
	if(currnet_working_to_find_current_key == False):
		th = threading.Thread(target=decrypt_encrypted_text)
		th.start( )
		currnet_working_to_find_current_key = True
		input_field.config(state=DISABLED)
		decrypt_button.configure(text='Click here to stop the proccess')
	else:
		currnet_working_to_find_current_key = False
		decrypt_button.configure(text='Decrypt Automatically')
		input_field.config(state=NORMAL)


title = Label(root, text="Substitution Cipher - Quadgram Statistics")
title.configure(bg='#79a0e8', fg='#3e6ec7', font=("", 12, "bold"))
title.pack(pady=(15,0))

desc = Label(root, text="Using quadgram analysis, the program will find the key that fits the most, and makes the ciphertext looks like english")
desc.configure(bg='#79a0e8', fg='#3e6ec7', font=("", 8, ""))
desc.pack()

input_field = Text(root, width=95, borderwidth=5, font=("default", 10), height=7)
input_field.configure(bg='#abc8ff')
input_field.pack(pady=10)
decrypt_button = Button(root, text="Decrypt Automatically", command=mid)
decrypt_button.pack(pady=10)
current_key = Label(root, text="Current substitution key")
current_key.configure(bg='#79a0e8', fg='#3e6ec7', font=("", 12, "bold"))
current_key.pack(pady=5)
decrypted_field = Text(root, width=95, borderwidth=5, font=("default", 10), height=7)
decrypted_field.configure(bg='#abc8ff')
decrypted_field.pack(pady=15)
root.mainloop()