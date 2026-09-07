Name : Delitha Theodora

NPM : 2506553585

Class : PBP KKI

### Tugas 1

1. Yes, I was pretty strict about using HTML5 semantic elements for the main structure. In base.html, I used <header>, <main>, <nav>, and <footer>. To separate the content sections, I utilized <section> (for example, <section class="hero"> and <section class="projects">). I also use the <picture> and <source> tags specifically to render different ID Card assets for desktop and mobile.

This helps a lot in static web development because:
- Clean & maintainable code: It's much neater and easier to pinpoint where the "Profile" or "Projects" component is compared to just stacking everything using <div> tags.
- Accesibility & SEO: Tags like <main> and <section> automatically build a clear document hierarchy, making it easier for screen readers and search engines to understand the page structure.

2. Honestly, the biggest layout challenges when setting up the responsive CSS were in the Projects and Profile sections. 

On Desktop, the Projects section uses a landscape folder graphic (metaphor) that holds the project cards using absolute positioning. The problem was, when transitioning to mobile, the folder shrank to stay proportional. As a result, the project cards inside piled up very badly, and the text became unreadable. For the Profile section, the challenge was figuring out how to turn a wide 3-column grid into a scrollable single stack on a phone.

How I evaluated and prioritized elements:
I prioritized readability and UX over forcing the desktop visual metaphor to stay.

- Projects Section Evaluation: Instead of forcing the cards into a tiny folder, I decided to hide the folder graphic on mobile (display: none). I pulled the cards out into a full-width carousel layout and changed their internal layout to vertical (flex-direction: column) so the images and text get maximum space.
- Profile Section Evaluation: Since forcing 3 columns on a phone screen would break the content, I changed the grid orientation to a single vertical column. I also swapped the ID Card asset (using the <picture> tag) with a mobile-id.svg version specifically designed with proportions for small screens. Finally, font sizes (especially for the large Genty headers) were scaled down using media queries so they look proportional and don't dominate the screen.

3. The main limitation of a pure static website is the heavy repetition in the code (violating the DRY principle) and the lack of scalability. Right now, every single project card in the portfolio has its HTML structure manually hardcoded. If i want to add a new project, edit a tech stack, or change the card layout, I have to manually copy-paste and edit the HTML blocks all over again, which is very prone to errors

Based on this limitation, the dynamic functionality I want to add in the next iteration is integrating Django's dynamic templating. I plan to migrate all the static project data (titles, descriptions, tech stacks, and image paths) into a backend (views.py). Then, I will replace the repetitive hardcoded HTML with a single, clean {% for %} loop to generate the project cards automatically based on the backend context, making the portfolio much easier to maintain.

AI Disclosure & Usage Log

Tools Used: Gemini, Figma.

Prompting Strategy: I utilized AI as a technical assistant throughout the development process. I actively used it to pinpoint the root causes of unfamiliar errors when I was stuck, determine exactly which code sections needed to be modified to achieve specific layout adjustments, and generate precise CSS syntax (such as background element rotations and implementing interactive animations). Additionally, it served as a thought partner for debugging deployment configurations (Django settings.py).

AI Limitations & Manual Improvements (Critical Reflection): While AI is excellent for syntax scaffolding and backend debugging, I found it highly limited in spatial reasoning for complex, overlapping CSS layouts. Consequently, the core UI implementation—specifically the absolute positioning within the desktop SVG folder graphic and the responsive mobile flexbox transitions—was executed manually based on my Figma design system. AI could provide generic media query syntax, but the actual visual evaluation, breakpoint prioritization, and "vibe coding" adjustments required strict human intervention to ensure usability.

Prompting Logs: 

"i added the images for the projects (oh-project.webp and ddp0-project.webp), where do i put the link to the proejcts"
"the cards r not centered why is that"
"the slide html code is very repetitive honestly, is there anyway to avoid that?"
"git switch or git checkout"
"i ran python manage.py check --deploy and got security warnings (W004, W009, W018). how do i fix that"
"im getting a 'missing-import' error for python-dotenv in vscode, how do i fix it?"