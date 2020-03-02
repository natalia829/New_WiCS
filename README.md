WiCS Comp is a website dedicated to Harvard students interested in comping
Women in Computer Science. The current comping process requires students to
submit a Google form stating the individual’s name, the event category, and
some sort of proof of attendance. The current comp process is inefficient for
compers due to the student’s inability to access the events they have successfully
comped. Due to this hindrance, Natalia Calvo, Alexa Lagunas, and Halle Clottey have
implemented a site specifically to keep track of the events students go to.

GETTING STARTED:
To run the web application, dowload the WiCS folder into your CS50 IDE. Then, retrieve
an API token on iexcloud.io (make an account first if you do not have one). Take note
of the key and within the CS50 IDE terminal, write export API_KEY=value. Afterwards,
write flask run in the terminal (make sure you are in the right folder). Then click
on the running link to begin.

RUNNING THE WEBSITE:
This web site has two main user experiences: the user interface--which is
for students comping Women in Computer Science--and the admin interface--which
is for the WiCS board members managing the site.

Admin Username: admin // Admin Password: 1

Under the user interface, students are able to register for their own login before
filling out a form specifying their name, the name of the event they attended, the
category of that event, and some sort of proof indicating that they were in attendance,
including submitting a photo. Once they fill in this form, they will wait for the admin
to approve or deny completion of this comp event. They are able to check the status
of all their submissions and their approval status through the Track Attencdance page.

Users are also able to view an updated calendar of the WiCS events taking
place this semester. For those interested in exploring more about Computer Science,
there is a resource page highlighting the Gender Gap in CS, websites to help compers
learn how to code, and information regarding summer opportunities (including
internships and research positions).

Under the admin interface, board members are able to approve or deny the attendance
of a comp event for a specific individual. After marking each entry, the database
will update the approval status of that particular event, notifying the user of
whether or not their submission was approved.

Overall, this website increases the efficiency of the comping process by allowing
users to track the events they have gone to. If they successfully comped the proper
number of events, then they are officially a part of Harvard’s Women in Computer
Science club!
