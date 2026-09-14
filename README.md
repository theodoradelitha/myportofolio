**Name:** Delitha Theodora  
**NPM:** 2506553585  
**Class:** PBP KKI  

---

**Project Setup Instructions**
1. Clone the repo: `git clone <your-repo-url>`
2. Go to the project folder: `cd <your-repo-name>`
3. Turn on the virtual environment: 
   * Mac/Linux: `source env/bin/activate`
   * Windows: `env\Scripts\activate`
4. Install requirements: `pip install -r requirements.txt`
5. Set up the database: `python manage.py migrate`
6. Run the server: `python manage.py runserver`
7. Open `http://localhost:8000` in your browser.

---

### Assignment 1

1. Yes, I was pretty strict about using HTML5 semantic elements for the main structure. In `base.html`, I used `<header>`, `<main>`, `<nav>`, and `<footer>`. To separate the content sections, I utilized `<section>` (for example, `<section class="hero">` and `<section class="projects">`). I also use the `<picture>` and `<source>` tags specifically to render different ID Card assets for desktop and mobile.

   This helps a lot in static web development because:
   * **Clean & maintainable code:** It's much neater and easier to pinpoint where the "Profile" or "Projects" component is compared to just stacking everything using `<div>` tags.
   * **Accessibility & SEO:** Tags like `<main>` and `<section>` automatically build a clear document hierarchy, making it easier for screen readers and search engines to understand the page structure.

2. Honestly, the biggest layout challenges when setting up the responsive CSS were in the Projects and Profile sections. 
   
   On Desktop, the Projects section uses a landscape folder graphic (metaphor) that holds the project cards using absolute positioning. The problem was, when transitioning to mobile, the folder shrank to stay proportional. As a result, the project cards inside piled up very badly, and the text became unreadable. For the Profile section, the challenge was figuring out how to turn a wide 3-column grid into a scrollable single stack on a phone.

   **How I evaluated and prioritized elements:**
   I prioritized readability and UX over forcing the desktop visual metaphor to stay.
   * **Projects Section Evaluation:** Instead of forcing the cards into a tiny folder, I decided to hide the folder graphic on mobile (`display: none`). I pulled the cards out into a full-width carousel layout and changed their internal layout to vertical (`flex-direction: column`) so the images and text get maximum space.
   * **Profile Section Evaluation:** Since forcing 3 columns on a phone screen would break the content, I changed the grid orientation to a single vertical column. I also swapped the ID Card asset (using the `<picture>` tag) with a `mobile-id.svg` version specifically designed with proportions for small screens. Finally, font sizes (especially for the large Genty headers) were scaled down using media queries so they look proportional and don't dominate the screen.

3. The main limitation of a pure static website is the heavy repetition in the code (violating the DRY principle) and the lack of scalability. Right now, every single project card in the portfolio has its HTML structure manually hardcoded. If I want to add a new project, edit a tech stack, or change the card layout, I have to manually copy-paste and edit the HTML blocks all over again, which is very prone to errors.

   Based on this limitation, the dynamic functionality I want to add in the next iteration is integrating Django's dynamic templating. I plan to migrate all the static project data (titles, descriptions, tech stacks, and image paths) into a backend (`views.py`). Then, I will replace the repetitive hardcoded HTML with a single, clean `{% for %}` loop to generate the project cards automatically based on the backend context, making the portfolio much easier to maintain.

<br>

**AI Disclosure & Usage Log (Assignment 1)**
* **Tools Used:** Gemini, Figma.
* **Prompting Strategy:** I utilized AI as a technical assistant throughout the development process. I actively used it to pinpoint the root causes of unfamiliar errors when I was stuck, determine exactly which code sections needed to be modified to achieve specific layout adjustments, and generate precise CSS syntax (such as background element rotations and implementing interactive animations). Additionally, it served as a thought partner for debugging deployment configurations (Django `settings.py`).
* **AI Limitations & Manual Improvements:** While AI is excellent for syntax scaffolding and backend debugging, I found it highly limited in spatial reasoning for complex, overlapping CSS layouts. Consequently, the core UI implementation—specifically the absolute positioning within the desktop SVG folder graphic and the responsive mobile flexbox transitions—was executed manually based on my Figma design system. AI could provide generic media query syntax, but the actual visual evaluation, breakpoint prioritization, and "vibe coding" adjustments required strict human intervention to ensure usability.
* **Prompting Logs:** 
  * `i added the images for the projects (oh-project.webp and ddp0-project.webp), where do i put the link to the proejcts`
  * `the cards r not centered why is that`
  * `the slide html code is very repetitive honestly, is there anyway to avoid that?`
  * `git switch or git checkout`
  * `i ran python manage.py check --deploy and got security warnings (W004, W009, W018). how do i fix that`
  * `im getting a 'missing-import' error for python-dotenv in vscode, how do i fix it?`

---

### Assignment 2

1. When a user opens the new portfolio page, the following sequence occurs:
   1) **Client Request:** The browser sends an HTTP request to the server (e.g., visiting `/blog/`).
   2) **Project `urls.py`:** The main project router receives the request and forwards it to the application's specific `urls.py` (e.g., `main/urls.py`).
   3) **Application `urls.py`:** This file maps the `/blog/` path to the corresponding function in `views.py` (e.g., `show_blog`).
   4) **View:** The view function asks the **Model** for the necessary data.
   5) **Model:** The `BlogPost` or `Project` model communicates with the database, retrieves the requested records, and hands them back to the view.
   6) **Template:** The view packages this database data into a context dictionary and sends it to the HTML **Template**. The template uses Django Template Language (DTL) to dynamically inject the data into the structure.
   7) **Response:** The server sends the fully rendered HTML back to the user's browser.

2. Storing portfolio data in a model makes the application dynamic, scalable, and easier to maintain. If projects were hardcoded into the template, adding a new project would require manually rewriting HTML, testing the UI, and deploying a new code update. By using a model, data is separated from the design. Future development becomes vastly easier (can add a Django Admin panel to add new projects via a GUI, implement search filters, or paginate blog posts without ever touching the frontend codebase).

3. - **`makemigrations`** acts as a blueprint maker. It scans `models.py` for changes and generates a Python script (a migration file) that records how the database schema needs to change. It does not touch the actual database.
   - **`migrate`** is the execution command. It reads the migration files and applies those structural changes directly to the database (e.g., creating tables or adding columns).

   **Example:** When I decided to add a `read_time = models.IntegerField()` field to my `BlogPost` model, I first had to run `python manage.py makemigrations` to create the instruction file, and then `python manage.py migrate` to actually add the `read_time` column to my database table.

<br>

**AI Disclosure & Reflection (Assignment 2)**

**1. Tools Used**
* Google Gemini

**2. Prompting Strategy**
I used AI more like a discussion partner rather than just asking it to generate the whole assignment. My approach was:
* **Clarifying concepts:** Before answering the theoretical assignment questions, I asked the AI to break down concepts like MVC vs. MTV and the exact difference between `makemigrations` and `migrate` so I could understand, then explain them in my own words.
* **Targeted problem-solving:** Instead of asking for entire files, I asked for specific syntax or best practices. For instance, I consulted the AI on how to implement custom model properties, add readable string representations (`__str__`), and set up pagination logic for scalable data rendering.
* **Workflow and debugging:** I used the AI as a technical sounding board to troubleshoot edge cases and errors. When my blog template didn't render after adding pagination due to a context variable mismatch, or when I hit Git warnings, I asked for diagnostic steps to debug the issue myself.

**3. Parts of the Project Assisted by AI**
* **Theoretical Documentation:** Helped me structure my understanding of Django's MTV architecture and database migration lifecycle for the README questions.
* **Model Best Practices:** Advised on implementing readable `__str__` representations and using the `@property` decorator for derived attributes without bloating the database.
* **Feature Exploration:** Provided guidance on using Django's built-in `Paginator` class and QuerySet sorting (`order_by`) to handle content growth gracefully.
* **Unit Tests & Debugging:** Guided me on proper assertions for empty states in `TestCase` and helped diagnose a template context name mismatch (`blog_list` vs. `page_obj`).

**4. Prompt History Log**
* `im trying to understand mtv vs mvc for the readme questions, can u explain it simply?`
* `what is the difference between makemigrations and migrate again? i can't really find the words`
* `how do I make it so that if my projects database is empty it shows a message instead of just blank? is it DTL?`
* `(env) delithatheodora@Delithas-MacBook-Pro-4 myportofolio % python manage.py runserver ... ImportError: cannot import name 'show_blog' from 'main.views'`
* `ok ive made the css and HTML template for blog, should I continue by adding content to the blog?`
* `how do I add a property in the model to check if a project is still ongoing?`
* `what is an impactful feature for the blog view to handle lots of posts? is paginator hard to set up?`
* `kok blog contentnya gone pas pagination ditambahin, padahal contextny udah dioper?`
* `what should I assert in tests.py for checking the empty state?`
* `oh no this branch says it cant automatically merge... how to resolve it without merging yet?`