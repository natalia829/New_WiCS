Application.py: We used the jinga environment in order to implement
our Python code. Line 35 ensures that we’re able to use SQL in
order to make a database and line 38 ensures that the API key is set.

Login is required to access all of these webpages.
“/” renders the template index.html, which is just the home page.
If the request is GET, “/approve” makes a dictionary and fills it
with the user’s id, name, event name, category, photo, and other
proof. This request renders the template approve.html. If the method
is POST, “/approve” inserts category into the events table.

 “/history” checks to see the type of event a student has attended. Each
 line of code within this section checks the count for each category of events:
 Large Social (ls), Small Social (ss), Sponsorship (sp), and Educational (ed).
 Compers are expected to attend at least one of each as well as two additional
 ones for a total of 6 events. The progress bar checks to see how far each person
 is in the comping process. Edu2 checks to see how many events they still need to
 attend. In the end, this page renders the template for history.html after appending
 the events in the dictionary.

“/login” requires users to enter a username and password before they’re able to
access the site. Usernames are stored in a database so that when the Select query
is used, the computer can find the specific user and ensure that their password
is correct. Once they are logged in, the site remembers which user was logged in.
“logout” just clears the session and redirects users to the login form.

“/attendance” tracks the attendance of each comper for each event. If the request
is GET, it renders the template attendance.html. If the request is POST, then it
requests the name, event name, category, photo and/or other proof, username,
and current time before inserting this information into the table of events.

“/register” requires that the users make a login and register for the site.
It checks to see if the two passwords entered are equal before entering the user
into the database.

TEMPLATES:

Apology.html: If data entered is invalid, then this apology is rendered and displayed.

Approve.html: This displays the database table for admin to view. They have to select
whether or not each event displayed is approved or not. Afterwards, they have to click
submit which alters the data underneath status to be “Approved” or “Not Approved.”

Attendance.html: This attendance form asks users for their name, the event they
attended, the category of the event, a photo verifying their attendance, or some
sort of other proof. The data they entered gets stored into the database and gets
updated on the admin’s end.

Index.html: This home page displays information about joining WiCS. It also includes
details about what happens after joining WiCS as well as information about the
leadership committee. The final portion of this page displays a Google Calendar of
WiCS events. This implementation makes it easy for compers to see when different
events are taking place so that they can carve out time in their schedule to attend
a comping event. This helps increase comping efficiency.

Layout.html: Layout utilizes bootstrap in order to beautify our site. This page
links to the styles sheet so that the CSS can be applied to all webpages. The
navigation bar allows users to access multiple attributes of the WiCS Comp Website.
Admin can access these tabs: Add Attendance, Track Attendance, Resources, Approve
Attendance, and Add to Calendar. Users can access these tabs: Add Attendance, Track
Attendance, and Resources. There is a logout button on the end when either user is
logged in and a login/register button for when no one is logged in. The end of each
page has All Rights Reserved written on the bottom to make the site more official.

Login.html: Provides the html that allow users to login. Refer to application.py
above for more details.

Register.html: Provides the html that allow users to register. Refer to application.py
above for more details.

Resources.html: Resources has many styles implemented into the page to make it more
appealing to look at and scroll through. The information under the Gender Gap in
Computer Science is displayed using a carousel. The images used were taken from Google
and used to quantify the actual gap in CS between men and women. The indicators
below the images and the arrows to the sides of the carousel allow the user to
navigate the 3 different slides so that they can read through the images at a pace
they are more comfortable with. The section under Learn How to Code directs users to
many websites that can help them learn how to code on their free time. The information
under Summer Opportunities lists different internships and research positions compers
can look through if they’re interested in spending their summers exploring more about
CS.

STATIC:

Styles.css: This CSS section targets the classes and ids detailed in the html pages.
Our design choices were made to make the site more aesthetically pleasing to view.
The soft greys, dark greys, black, white, and pinkish salmon colors were inspired by
the original WiCS website. These colors are inviting and easy on the eyes. Centering
most of website was also done purposefully. Since there is not a lot of information
written on each page, center-aligning our code makes our site easier to read through
and navigate.


