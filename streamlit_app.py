import streamlit
# import pandas as pd
# import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Dinner')
streamlit.header('Breakfast Menu')
streamlit.text('π₯£ Omega 3')
streamlit.text('π₯ Kale, Spinach')
streamlit.text('πHard Boilded')
streamlit.text('π₯π Avocado Toast')

streamlit.header('ππ₯­ Build Your Own Fruit Smoothie π₯π')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
#streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

#New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

## fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
## streamlit.text(fruityvice_response.json()) #just writes the data to the screen

# write your own comment -what does the next line do? 
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)



streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
streamlit.text("Hello from Snowflake:")
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from fruit_load_list")

## fetch one row into text line
# my_data_row = my_cur.fetchone() ## fetch one row
# streamlit.text("The fruit load list contains:")
# streamlit.text(my_data_row)

## fetch one row into table
# my_data_row = my_cur.fetchone() ## fetch one row
# streamlit.header("The fruit load list contains:")
# streamlit.dataframe(my_data_row)

## fetch all rows into table
my_data_row = my_cur.fetchall() ## fetch all rows
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

# add fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like information about?','Kiwi')
my_cur_add = my_cnx.cursor()
my_cur_add.execute("insert into fruit_load_list values(" + add_my_fruit + ")")

streamlit.write('Thanks for adding ', add_my_fruit)
