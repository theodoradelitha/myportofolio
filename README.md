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

### Weekly Progress / Changelog

*   **Week 1 (Assignment 1):** Built the static portfolio using HTML5 and CSS. Implemented a responsive layout, including absolute positioning for the desktop folder UI and a mobile-friendly flexbox structure.
*   **Week 2 (Assignment 2):** Migrated the static site to Django. Implemented the MTV architecture, created Project and BlogPost models, and set up dynamic template rendering and database migrations.
*   **Week 3 (Assignment 3):** Implemented full CRUD (Create, Read, Update, Delete) operations for the Projects, Blog, and Experience sections using Django ModelForm. Added JSON serialization endpoints and responsive UI enhancements (mobile hamburger menu, delete confirmation modals).

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

---

### Assignment 3

1. **Why use Django’s `ModelForm` instead of manual HTML forms? Why add `{% csrf_token %}`?**
   **Why ModelForm:**
   * **No Repetition (DRY):** When we manually write HTML forms, we have to recreate every single input field that already exists in the database model. `ModelForm` reads the model and generates the correct HTML inputs (like text fields, dropdowns, and date pickers) automatically.
   * **Automatic Validation:** `ModelForm` automatically enforces the rules defined in the models (like `max_length` or `choices`). If a user inputs invalid data, the form catches it without us having to write manual Python or JavaScript validation logic.
   * **Easy Saving:** Because the form is tied directly to the model, saving a new database entry is as simple as calling `form.save()`.
   
   **Why `{% csrf_token %}`:**
   * **Security:** CSRF (Cross-Site Request Forgery) is a common attack where a malicious website tricks a user's browser into submitting a harmful request to the website. The `{% csrf_token %}` generates a unique, hidden, and encrypted string on the form. When the form is submitted, Django checks this token to guarantee that the request legitimately originated from the website and not a hacker's script.

2. **Why is JSON preferred over XML in modern web development?**
   While both formats are used to transmit data, JSON is preferred in the modern web for a few reasons:
   * **Native to JavaScript:** JSON (JavaScript Object Notation) is natively understood by JavaScript. In modern web dev (like React, Vue, or vanilla JS), turning a JSON response into a usable object takes exactly one line of code (`response.json()`), whereas XML requires heavy and complex DOM parsing.
   * **Lightweight and Readable:** XML relies on heavy opening and closing tags for every piece of data (e.g., `<name>Delitha</name>`). JSON simply uses lightweight brackets and quotes (e.g., `"name": "Delitha"`). This makes JSON files smaller, faster to transmit over the network, and easier for humans to read.
   * **Data Structures:** JSON maps perfectly to modern programming structures like Arrays (Lists) and Objects (Dictionaries), whereas XML is purely a document tree.

3. **What is the flow when returning portfolio data in JSON? Why serialize Django models?**
   **The Flow:**
   * **The Request:** A user (or frontend code) accesses a URL like `/api/experience/`.
   * **The Query:** The Django view function (`get_experience_json`) queries the database to retrieve the raw data (e.g., `Experience.objects.all()`).
   * **The Serialization:** Django passes this QuerySet into the serialization engine, which translates the data into a JSON string.
   * **The Response:** The view returns an `HttpResponse` containing the JSON string, tagging it with `content_type="application/json"` so the browser knows exactly what it's receiving.
   
   **Why Serialization is Required:**
   When you query the database in Django, it returns a `QuerySet` containing complex Python Objects (your models). Web browsers, mobile apps, and frontend JavaScript cannot read Python objects. Serialization is the necessary translation process that takes complex, language-specific objects in memory and flattens them into a universal, plain-text format (JSON) that can be easily sent over the internet and understood by any other language or system.

<br>

## AI Usage Disclosure

For this assignment, I utilized AI as a targeted learning assistant to bridge the gap between the course tutorials and my specific project requirements.

**Tools Used:** Gemini

**Prompt Strategy:** 
To ensure I was actually learning the material, I avoided pasting my entire codebase into the prompt. Instead, my strategy was to ask targeted, conceptual questions (e.g., "how does the update view work in django?") or request isolated code snippets and hints to understand the logic before implementing it myself. 

**Specific Assisted Parts:**
*   **Projects CRUD:** The foundational `Create` and `Read` operations for my Projects section were adapted directly from Tutorial 3. 
*   **Update & Delete Logic:** When extending the tutorial logic to include `Update` and `Delete` functionalities, I asked the AI for conceptual hints on how to pass instance data to a `ModelForm` and how to structure a delete confirmation modal.
*   **Model Replication:** I applied the concepts learned from the Projects section to manually replicate the full CRUD structure for my **Blog** and **Experience** sections, occasionally asking the AI for syntax reminders.
*   **Git Best Practices:** I used the AI to help format conventional commit messages (e.g., `feat:`, `fix:`, `style:`) to maintain a clean, atomic Git history.

**Critical Analysis of AI Limitations & Manual Fixes:**
While the AI was excellent at explaining Django backend logic, it lacked the holistic context of my frontend design. 
*   **CSS Variable Hallucinations:** At one point, the AI suggested button classes using CSS variables that didn't exist in my stylesheet, resulting in invisible text buttons. I had to manually debug my `style.css` and direct the AI to use my existing theme variables.
*   **Layout Breakages:** When asking for a fix for a mobile layout issue, the AI suggested applying an inline `flex-direction: column` style. While this fixed the mobile view, it completely broke the desktop view. I had to manually discard the AI's inline style and implement proper responsive media queries in my CSS file instead.

**Prompting History/Log:**
*   how do i pass an existing project's data into a django modelform so the fields are already filled out when i try to update it?
*   what is the best way to handle a delete confirmation in django without making a whole new page? can i just use a popup card like thing?
*   im copying my projects crud structure for my blog and experience sections, but i want to use the same form template. how do i make the button text dynamic (like saying "add" vs "update")?
*   i dont quite understand how serialize works, can you try to teach me?
*   my edit and delete buttons are completely invisible on the project cards lmao
*   whats a great way for me to organize the overflowing navbar in mobile?
*   what are the best practices for git commit messages?

---

### Weekly Progress Update (Week 4 / Assignment 4)
* **Week 4 (Assignment 4):** Integrated Django's built-in authentication system. Implemented login, registration, and logout functionalities with proper session and cookie management. Established role-based access control by enforcing server-side permissions (`has_perm`) and conditionally rendering UI action buttons (`perms`) for Superusers and a custom "Editor" group. Finally, added an interactive ManyToMany "Star" feature for Projects and Blogs, ensuring JSON endpoints securely use natural foreign keys.

---

### AI Disclosure & Reflection (Assignment 4)

**1. Tools Used:** Gemini

**2. Prompting Strategy:**
For this assignment, my prompt strategy shifted towards architecture and access control theory. Rather than asking the AI to write the authentication views (which I implemented myself following the tutorial), I used the AI to understand how to extend the standard authentication flow into a Role-Based Access Control (RBAC) system. I focused my prompts on learning how Django's permission framework interacts with templates and how to securely manage ManyToMany database relationships without leaking sensitive user IDs in my API.

**3. Specific Assisted Parts:**
* **Role-Based Access Control (RBAC):** I struggled with how to check for an "Editor" role. The AI explained the difference between checking `request.user.groups` and using `request.user.has_perm()`. I then manually wrote the `has_perm` conditions in my `views.py` and the `{% if perms... %}` logic across all my HTML templates.
* **Security & JSON APIs:** When my `starred_by` feature started leaking raw User IDs in the `/api/projects/` endpoint, I asked the AI why that was happening. It pointed out the need for natural foreign keys, and I manually added `use_natural_foreign_keys=True` to my serializer parameters.
* **Many-To-Many Operations:** I consulted the AI to understand the syntax for adding and removing objects from a ManyToMany relationship (like `.add()` and `.remove()`), which I then used to structure my own `toggle_star` view.

**4. Critical Analysis of AI Limitations & Manual Fixes:**
* **Context Blindness in Templates:** When I asked the AI conceptual questions about template tags (like how to hide buttons based on permissions), it provided generic `{% if %}` block examples that completely ignored my specific UI structure and CSS classes. I couldn't just copy-paste; I had to carefully manually integrate the logic into my complex flexbox layout so the design wouldn't break.
* **Overcomplicating Simple Tasks:** When I first asked how to implement the "Editor" role, the AI suggested I build custom template tags and complex middleware. I had to critically evaluate its suggestion, realize it was massive overkill for this assignment, and guide the AI back to explaining the simpler, built-in Django `Permissions` framework.
* **Security Oversights in Examples:** When the AI explained how to structure update and delete views based on permissions, its examples lacked the `@login_required` decorators. If I had blindly followed its examples, unauthenticated visitors would have triggered unhandled 403 errors instead of being safely redirected to the login page. I had to manually audit my code and add those decorators myself.

**5. Prompting History/Log:**
* *how do i make a registration form using django's built-in UserCreationForm?*
* *i followed the tutorial for login but where do i set the cookie to store the last login time?*
* *my logout button is redirecting me to an error page, what url name should i use for it in urls.py?*
* *if i have a manytomanyfield for stars, how do i count how many people starred it in the html template?*
* *how do i check if a user is logged in inside my html file so i can hide the star button for guests?*
* *Test Unauthenticated Visitor: Try to open /projects/add/ but i get a 403 forbidden instead of a redirect. am i actually still logged in?*
* *my api is showing [1, 2] for starred_by, how do i make it show the actual usernames instead in get_projects_json?*

---

### Weekly Progress Update (Week 5 / Assignment 5)
* **Week 5 (Assignment 5):** Refactored the application to use asynchronous JavaScript (AJAX). Replaced standard page loads with `fetch()` API calls to retrieve JSON data from the backend. Implemented interactive, non-blocking UI states (loading skeletons, empty states, error handling) and debounced search fields across all major sections (Projects, Blog, Experience). Transitioned form submissions into Popover Modals using AJAX POST requests with strict CSRF token headers and DOM-based XSS sanitization.

---

### Assignment 5

1. **Explain what debouncing is and why this technique is important to implement in a search feature that uses AJAX.**
   Debouncing is a programming practice used to ensure that time-consuming tasks do not fire so often that they stall the performance of the application. In a search feature using AJAX, if debouncing is not used, an HTTP request would be fired to the server for every single keystroke. This would flood the server with unnecessary requests and cause severe performance issues. By using debouncing (e.g., waiting 500ms after the user stops typing), we drastically reduce server load and ensure only the final, meaningful search term is sent.

2. **Explain the purpose of using `await` when we use `fetch()`. What would happen if we did not use `await`?**
   `fetch()` is an asynchronous JavaScript function that returns a Promise. The `await` keyword pauses the execution of the `async` function until that Promise is resolved (meaning the server has fully responded). If we did not use `await`, the code would continue executing immediately before the data was actually retrieved from the server. This would result in variables holding unresolved Promise objects instead of the actual JSON data, which would break the DOM rendering logic and result in undefined content on the screen.

3. **Explain what a Cross-Site Scripting (XSS) attack is and why data displayed through AJAX/JavaScript is more vulnerable to this attack than data displayed directly through a Django template.**
   Cross-Site Scripting (XSS) is a security vulnerability where an attacker injects malicious scripts (like JavaScript) into trusted websites (e.g., typing a `<script>` tag into a Blog's content field). 
   When data is displayed directly through a Django template using `{{ variable }}`, Django's template engine automatically escapes special characters by default (converting `<` to `&lt;`), preventing scripts from running. However, when data is fetched via AJAX and manually inserted into the DOM using JavaScript (especially using properties like `innerHTML`), the browser will execute any unescaped scripts contained in that data. This makes AJAX heavily reliant on explicit manual escaping (like building a custom `escapeHtml()` function) and strict server-side sanitization (like Django's `strip_tags()`) to stay secure.

<br>

### AI Disclosure & Reflection (Assignment 5)

**1. Tools Used:** Gemini

**2. Prompting Strategy:**
For this assignment, my prompt strategy was strictly focused on understanding asynchronous JavaScript flow and security protocols. Instead of asking for entire template rewrites, I isolated my questions to specific mechanisms, such as how to securely pass CSRF tokens via headers in a `fetch()` request, or how JavaScript handles Promises differently than synchronous Python code.

**3. Specific Assisted Parts:**
* **AJAX Setup & CSRF:** I used the AI to help me understand how to extract the CSRF token from browser cookies and attach it correctly to the `X-CSRFToken` header of my POST requests.
* **Debouncing Logic:** I consulted the AI to explain the mechanics of `setTimeout` and `clearTimeout` to build a clean debouncer for my search bars.
* **UI/UX Enhancements:** I utilized the AI to help me generate the CSS keyframes (`@keyframes`) and `linear-gradient` logic required to build the advanced shimmering Skeleton Loading animation that I implemented for my loading states.

**4. Critical Analysis of AI Limitations & Manual Fixes:**
* **DOM Target Hallucinations:** The AI often provided generic JavaScript that didn't match the specific IDs and class names in my existing HTML structure. I could not copy-paste its DOM manipulation code; I had to manually rewrite its `document.getElementById` and `.innerHTML` logic to target my specific containers and ensure my loading, error, and empty states toggled correctly.

**5. Prompting History/Log:**
* *why is my fetch POST returning a 403 forbidden error when i try to add a project?*
* *what is the best way to clear the form inputs inside my modal after a successful AJAX submission?*
* *i want to make a skeleton loading animation in css, how does the linear-gradient shimmer effect work?*
* *my debounced search is working, but it keeps showing "no projects added yet" when my search just didn't find anything. how do I make it say "no projects found matching X"?*

---

### Tutorial 07: DRF API
The Projects page now loads and changes data through a Django REST Framework API instead of the hand-built `JsonResponse` views. The code lives in `main/serializers.py`, `main/permissions.py`, `main/api_views.py` and `main/api_urls.py`, and the tests are in `main/tests_api.py`.

| Method | Endpoint | Action | Who can do it |
|---|---|---|---|
| GET | `/api/v1/projects/` | List projects, `?title=...` to search | Everyone |
| POST | `/api/v1/projects/` | Add a project | Superuser |
| GET | `/api/v1/projects/<uuid>/` | Project detail | Everyone |
| PUT / PATCH | `/api/v1/projects/<uuid>/` | Update a project | Superuser |
| DELETE | `/api/v1/projects/<uuid>/` | Delete a project | Superuser |
| POST | `/api/v1/projects/<uuid>/star/` | Star / unstar | Logged-in users |

* Requests are authenticated with the normal login session (`SessionAuthentication`), so writes from the browser need the `X-CSRFToken` header.
* The Editor group can't write through this API, but it can still add, edit and delete projects through the existing HTML pages (`/projects/add/`, `/projects/<uuid>/update/`, `/projects/<uuid>/delete/`).
* The old `/api/projects/` and `/projects/add-ajax/` endpoints are still there for now.

Run the tests with `python manage.py test main`.

---

### Weekly Progress Update (Assignment 6)
**Assignment 6:** Implemented a Django REST Framework API for the Blog section by following the pattern from Tutorial 07. I created a `BlogPostSerializer` to handle data conversion and validation, including cleaning HTML tags from user input and checking that the title, content, and reading time meet the requirements. I also added role-based permissions so visitors and regular users can view articles, logged-in users can star them, Editors can create and update articles, and only the portfolio owner can delete them.

I added API endpoints for listing, searching, creating, updating, deleting, and starring blog posts. I also updated the Blog page to use JavaScript `fetch()` requests, allowing users to perform these actions without reloading the page. The add/edit modal supports partial updates, so it only sends the fields that have changed. I included CSRF protection and added tests for permissions, validation, starring, and API behavior across different user roles. I also removed the old Blog endpoints that were replaced by the new DRF API.

---

### Assignment 6

**1. Explain what REST means and why returning JSON alone isn't enough to call an API RESTful. Also explain the difference between PUT and PATCH, with an example of when each should be used.**

REST (Representational State Transfer) is an architectural style for building APIs around resources. Each resource has its own URL, and we use HTTP methods to perform different actions on it, such as GET to retrieve data, POST to create something, PUT or PATCH to update something, and DELETE to remove it.

Returning JSON alone doesn't make an API RESTful. In my previous implementation, I already returned JSON using `get_blogs_json` and `create_blog_ajax`, but the endpoints were still based on specific actions rather than resources. For example, I had a separate `/blog/add-ajax/` endpoint for creating a blog post. In Assignment 6, I changed this to use resource-based URLs:

- `/api/v1/blog/` for retrieving all blog posts or creating a new one.
- `/api/v1/blog/<uuid>/` for retrieving, updating, or deleting a specific blog post.

The HTTP methods also determine what action is performed, and the API returns appropriate status codes depending on the result.

The difference between PUT and PATCH is that **PUT updates the entire resource**, while **PATCH only updates specific fields**. For example, if I use PUT to update a blog post, I need to send all the required fields, such as its title, content, and read time. If I only send the title, the request will return a 400 error because the other required fields are missing.

Meanwhile, PATCH allows me to update only the fields I want to change. In my project, I use PATCH in the edit modal because users might only want to change the title without having to send the entire blog post again.

**2. Explain the role of a serializer in Django REST Framework. What are its advantages over manually assembling a dictionary with JsonResponse as in Tutorial 05?**

A serializer is used to convert model instances into data that can be sent as JSON, and also to convert incoming data into Python data that Django can validate and save.

In my assignment, I created `BlogPostSerializer` using `ModelSerializer`. Compared to manually creating a dictionary with `JsonResponse` like I did before, using a serializer has several advantages:

- **Less manual work:** I don't have to manually select and put every model field into a dictionary. I can define the fields I want to expose in one place.
- **Built-in validation:** The serializer can validate incoming data before saving it. I also added custom validation for the title, content, and read time. For example, titles and content cannot be empty or contain only HTML tags.
- **Read-only fields:** I can specify fields that users should not be able to change, such as the post ID, date posted, and star count. This prevents users from modifying information that should be controlled by the server.
- **Consistent responses:** The same serializer is used across different API endpoints, so the structure of the returned data stays consistent.
- **Safer data exposure:** I can control exactly which fields are included in the response. For example, I only expose the usernames of users who starred a post, not their private information.

Overall, serializers make handling and validating data easier compared to manually building dictionaries and handling everything myself with `JsonResponse`.

**3. Explain the difference between authentication and authorization in Django REST Framework. Why must access rights be checked with a permission class on the server, rather than only by hiding a button in the template?**

Authentication is about identifying who the user is, while authorization is about checking what that user is allowed to do.

In my project, I use `SessionAuthentication`, which allows Django REST Framework to identify users based on their existing login sessions. After that, permission classes determine whether they are allowed to perform certain actions.

For example, in my Blog API:
- Anyone can view blog posts, including visitors who haven't logged in.
- Only the Editor and superuser can edit blog posts.
- Only the superuser can create and delete blog posts.
- Any logged-in user can star a blog post.

I also use different permission classes depending on the endpoint, such as `IsAuthenticated` for the star endpoint.

Checking permissions only in the template is not enough because hiding a button doesn't actually prevent someone from accessing the endpoint. They could still send a request directly using Postman, curl, or the browser console.

That's why permissions need to be checked on the server using a permission class. Even if someone manually sends a DELETE request, the server will still check whether they are allowed to do it. In my tests, I also tried sending requests as different types of users and checked that unauthorized requests returned 403 without changing anything in the database.

**4. Explain why requests that change data still need a CSRF token when an API uses SessionAuthentication. Why isn't a test using force_authenticate enough to prove that CSRF protection works?**

When using `SessionAuthentication`, Django identifies the user through their session cookie. The problem is that browsers automatically send session cookies with requests to the website. This means that if a user is logged in, another website could potentially trick their browser into sending an unwanted request using that same session.

This is where CSRF protection comes in. A CSRF token helps verify that the request actually comes from our application. In my project, I send the token through the `X-CSRFToken` header whenever I make a request that changes data, such as POST, PUT, PATCH, or DELETE. I retrieve the token from the browser's cookies using `getCookie('csrftoken')`.

As for testing, `force_authenticate` is not enough because it directly assigns a user to the request without going through the normal authentication process. This means it skips the CSRF checks that happen with `SessionAuthentication`.

To properly test CSRF protection, I use `APIClient(enforce_csrf_checks=True)` together with `client.login()`. This allows the test to use an actual session and enforce CSRF checks. I then test requests both without and with a valid CSRF token to make sure that requests without one are rejected with a 403 response, while valid requests are accepted.

### AI Disclosure & Reflection (Assignment 6)

**1. Tools Used:** Claude (Claude Code)

**2. Prompting Strategy:**

For this assignment, my prompting strategy focused on understanding how Django REST Framework works and how its components interact when building a REST API. Rather than relying on AI to generate an entire implementation without understanding it, I used it to clarify specific concepts, understand the differences between the existing Django implementation and the new DRF approach, and troubleshoot issues during development. I focused particularly on serializers, permission handling, HTTP methods, and integrating API responses with the existing JavaScript frontend.

**3. Specific Assisted Parts:**

- **DRF Serializers & Validation:** I used AI to help me understand how `ModelSerializer` works, how to define explicit fields, and how serializers handle data validation. I also asked for clarification on implementing custom validation methods such as `validate_title()` and `validate_content()`.

- **Authentication & Permissions:** I consulted AI to understand how to implement role-based access using custom DRF permission classes. This included understanding how the portfolio owner, Editor, regular users, and anonymous visitors should interact with the Blog API.

- **API Integration & HTTP Methods:** I used AI to clarify how GET, POST, PUT, PATCH, and DELETE requests work in the context of REST APIs. I also received guidance on connecting the existing Blog page to the new DRF endpoints using JavaScript `fetch()` requests without requiring full page reloads.

- **CSRF Protection:** I asked AI for help understanding how Django's `SessionAuthentication` works with CSRF protection, particularly why write requests need to include the `X-CSRFToken` header and how to test CSRF enforcement.

- **Testing & Debugging:** I used AI to help understand how to structure API tests using `APITestCase`, including testing different user roles, validation errors, response status codes, and database changes after API requests.

**4. Critical Analysis of AI Limitations & Manual Fixes:**

- **Existing Project Context:** AI sometimes suggested implementations based on generic DRF patterns that did not fully account for my existing portfolio structure. I had to consider the existing `BlogPost` model, forms, views, templates, and permission logic before applying suggestions.

- **Permission Logic:** The role requirements were particularly important because the existing Django views had permission checks that did not completely match the assignment's requirements. I needed to examine the existing role configuration and ensure that the API permissions and HTML page visibility followed the intended rules.

- **Frontend Integration:** Generic JavaScript suggestions could not always be applied directly to my existing Blog page. I had to account for the actual HTML structure, existing CSS classes, loading and error states, and the way the page previously handled AJAX requests.

- **Understanding Test Results:** AI assistance helped me identify potential edge cases, but I still needed to examine test results and understand what they meant, especially when checking whether unauthorized requests left the database unchanged and whether the existing Tutorial 07 Projects API continued working correctly.

**5. Prompting History/Log:**

- *what's the difference between a django rest framework serializer and manually returning like a jsonresponse?*
- *how does modelserializer work, and how can i add custom validation for individual fields?*
- *how shud i implement a custom permission class for an API with an owner, editor, regular users, and anonymous visitors?*
- *when shud i use PUT instead of PATCH when updating an existing resource?*
- *why does SessionAuthentication require a CSRF token for POST, PUT, PATCH, and DELETE requests?*
- *how can i test API permissions and CSRF protection using APITestCase and APIClient?*
- *how can i update my existing js frontend to use drf endpoints without reloading the page?*
