import streamlit as st
st.title("MedicationTracker")
st.write("The latest technology [AI] is making working with the oldest technology[pen and paper] a whole lot easier, the Medication Tracker utilizes Azure AI Document Intelligence to extract medication tracker data from PDF files and save it as digital data. I have developed  a simple form to track medication intake by using pen and paper. This is  a hassle free and more natural way of tracking progress on intake rather than ‘tinkering’ with digital devices which often need WIFI, power, internet, subscription to operate. When its all done you will need a device to upload the PDF 😊.Please follow instructions to test how well the solution extracts data from raw to digital.  There is a Review page to check accuracy of the output, particularly hand written recording. Remember to use FICTITIOUS information as this solution is STRICTLY for testing purposes. Alternatively, you can download a pre-filled form and use it for testing. Please remember to leave a comment on the comment page or via email.")
import streamlit as st
st.title("Instructions")
st.header("Follow exact instructions")
st.subheader("Step 1.")
st.write("First go to the download page and either download or print the form you select. Completed sample forms are provided to make testing quicker (download and upload), however, you can print the form and fill it out. This is a test so do not use any real information use pseudo information to fill the form.")
st.subheader("Step 2.")
st.write("After filling the form, Go to the upload page and select your filled form and click submit. If all goes well it should say File uploaded successfully!, you may now move on to the review page")
st.subheader("Step 3.")
st.write("Check accuracy and edit the form accordingly *Note that innacuracies may be caused by illegible handwriting* .")
st.subheader("Step 4")
st.write("Go to your Dashboard to view your results.")
st.header("Final Step")
st.write("Leave a comment")

