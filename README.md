# Campus Sport Connect

### GOAL
Campus Sports Connect aims to bring students at the University of Illinois Urbana-Champaign (UIUC) together for sports activities by providing a platform to easily coordinate and participate in events. The app allows users to create, discover, and join sports events based on their preferences and availability. By enabling features like user notifications, profile management, and event updates, the platform fosters a more active and connected campus community.

### Functionality 
1. Event Creation: Users can create new sports events by specifying the sport type, required number of participants, date, time, and location. Besides, the background image would be automatically selected based on our keyword detection results. 
2. Communication: Users can get access to other participants by clicking their avatars and communicating with them via their provided telephone numbers.   
3. Event Discovery: Users can browse and search for upcoming sports events.
4. Event Participation: Users can join events, updating the participant count (e.g., from 2/10 to 3/10) but never surpass the participants limit. Joining past events would not be allowed. 
5. User Accounts: Users can create and manage their accounts using their university email addresses and Gmail. 
6. Profile Management: Users can update their profiles, including preferred sports, avatars, and phone numbers.
7. Database Management: Implemented an SQLite database for user and event data. Manually resolved merge conflicts in binary database files during collaborative development.
8. Responsive Design: Ensured a user-friendly interface with Bootstrap for a seamless experience across devices.
   
### Technical Architecture
<img width="691" alt="e605deec123b4082f24c513ec007f90" src="https://github.com/user-attachments/assets/5569ee32-e792-4990-9bae-d81c8824861d">

### Contributions
Yuemin Yu:
1. Designed the website's UI, including button layout and visual effects.
2. Implemented user authentication, including registration, login, and logout functionalities.
3. Keyword detection to select background images automatically. 

Chris Wu: 
1. Contributed to setting up the SQLite database and integrating Flask-Login.
2. implemented the profile management system, allowing users to personalize their accounts.
3. Added time and date selection in creating events.

Tiger Gao:
1. Developed the front end, including the main page layout and background image options.
2. Refined the profile management system by allowing users to provide their telephone numbers.
3. Implemented test cases for our project, and tested and debugged the application to ensure stability and performance.

Ke Yao:
1. Enhanced UI/UX for the "View My Events" and "View All Events" pages by categorizing events into upcoming and past sections.
2. Added features for event discovery and participant listing with profile hyperlinks.
3. Edited and refined database, allowing our new features such as "telephone numbers" and new "background" image options work properly.  


### Official Website 

(https://campus-sports-connect.vercel.app/)
