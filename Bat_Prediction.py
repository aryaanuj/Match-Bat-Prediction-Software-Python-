import tkinter as tk
from tkinter import ttk 
import mysql.connector 


root = tk.Tk()
root.geometry("600x300+300+100")
root.title("Bat Prediction")

con = mysql.connector.connect(host='localhost', username='root', database="bat_prediction")
curs = con.cursor()
query = "SELECT * FROM players"

curs.execute(query)
team1 = dict(curs.fetchall())


#label frame
label_frame = ttk.LabelFrame(root, text="Bat Prediction")
label_frame.grid(row=0, column=0, padx=100, pady=10)

#player label
player_label = ttk.Label(label_frame, text="Choose Player :")
player_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

keys_v = list(team1.keys())
keys_list = keys_v.copy()
keys_list.insert(0,"Select Player")
#player entry
player_entry = tk.StringVar()
player_entry1 = ttk.Combobox(label_frame, width=40, textvariable=player_entry, state="readonly")

player_entry1['values'] = keys_list
player_entry1.current(keys_list.index("Select Player"))
player_entry1.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

#predicted player
predicted_player = ttk.Label(label_frame, text="predicted player : ")


predicted_label = ttk.Label(label_frame)


history_name = ['abc']
#function
def func():
	global history_name
	global keys_list
	if len(keys_list) > 1:
		if player_entry.get() == "Select Player":
			predicted_label.configure(text="Please choose player!")
		else:
			player = str(player_entry.get()).lower()
			if player in history_name:
				predicted_label.configure(text="This player has already choosen!!")
				keys_list.remove(player_entry.get())
				player_entry1.configure(values=keys_list)
				player_entry1.current(keys_list.index("Select Player"))

			else:
				try:
					choosen_player_score = 'a'
					p_score = [ ]
					p_name = [ ]
					for keys, values in team1.items():
						team1[keys.lower()] = team1.pop(keys)

					choosen_player_score = team1[player]
					keys_list.remove(player_entry.get())
					player_entry1.configure(values=keys_list)
					player_entry1.current(keys_list.index("Select Player"))
					team1.pop(player)
					history_name.append(player)
					
					
					count = 0
					for i in team1:
						if choosen_player_score <= team1[i]:
							p_score.append(team1[i])
						else:
							count += 1

					if count == len(team1):
						for j in team1.values():
							p_score.append(j)
						p_score.sort()
						m = len(p_score)
						p_name=[player_name for player_name, score in team1.items() if score == p_score[m-1]]
						predicted_label.configure(text=p_name[0])
						team1.pop(p_name[0])
						history_name.append(p_name[0])
						keys_list.remove(p_name[0].title())
						player_entry1.configure(values=keys_list)
						player_entry1.current(keys_list.index("Select Player"))
	
					else:
						n = len(p_score)
						if n > 0:
							p_score.sort()
							p_name=[player_name for player_name, score in team1.items() if score == p_score[n-1]]
							predicted_label.configure(text=p_name[0])
							team1.pop(p_name[0])
							history_name.append(p_name[0])
							keys_list.remove(p_name[0].title())
							player_entry1.configure(values=keys_list)
							player_entry1.current(keys_list.index("Select Player"))
				except:
					return							
	else:
		predicted_label.configure(text="All players have been choosen!!")	
		


predicted_player.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
predicted_label.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

#button
predict_btn = ttk.Button(label_frame, text="Predict", command=func)
predict_btn.grid(row=2, column=1, padx=5, pady=30, sticky=tk.W)



root.mainloop()