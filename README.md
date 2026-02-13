Update this file with any extraneous info!


Current admin sign-in -

Email: admin@talenttrek.com (btw this is not a real email)

Password: adminpassword


Test User sign-in -

Email: test@talenttrek.com

Password: testuserpassword


The registration and login should now make a new TTUser object. It requires a unique email instead of a username but still gives each user an ID.

Then the Recruiter and Job Seeker have OneToOneFields for their user connecting back to the TTUser object. This allows for the registration/login to occur before doing the onboarding functions.


Setup Wizard - Visually functions, still doesn't save all inputs somewhere as it's entirely frontend work


Note - Use 'pip install django-cities-light' for location-based data
