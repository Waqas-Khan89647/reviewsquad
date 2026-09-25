# START HERE: simple step-by-step guide

Do the steps in order. Don't skip any.
If something goes wrong, take a screenshot and ask for help.

**How to type a command:** in IBM Bob, click the menu **Terminal → New Terminal**.
A black box opens at the bottom. Click inside it, type (or paste) the command, and press **Enter**.
Wait until it finishes before typing the next one.

---

## STEP 1: Install Python
1. Go to **python.org/downloads** and click **Download Python**.
2. Open the downloaded file.
3. ✅ **Tick "Add python.exe to PATH"** at the bottom of the window. This is very important.
4. Click **Install Now**. When it finishes, click **Close**.

## STEP 2: Install Git
Git saves versions of your code and uploads it to GitHub.
1. Go to **git-scm.com/download/win**. The download starts.
2. Open the file and click **Next** on every screen, then **Install**.

## STEP 3: Restart Bob and check
1. Close IBM Bob completely and open it again.
2. Open a terminal (**Terminal → New Terminal**) and type:
   ```
   python --version
   ```
   You should see `Python 3.x.x`.
3. Then type:
   ```
   git --version
   ```
   You should see `git version ...`.

## STEP 4: Open the project in Bob
1. Right-click `reviewsquad.zip` → **Extract All** → choose `C:\Projects` → **Extract**.
2. In Bob: **File → Open Folder** → choose `C:\Projects\reviewsquad` → **Select Folder**.
3. If Bob asks "Do you trust the authors?", click **Yes, I trust**.
4. On the left you should see folders like `sample_app`, `reviewsquad` and `team_docs`.

## STEP 5: Prepare Python for this project
In the terminal, type these one by one:
```
python -m venv .venv
```
```
.venv\Scripts\activate
```
Now the line should start with `(.venv)`.

> ❗ If you see a red error saying *"running scripts is disabled"*, type this once, then run
> the `activate` command again:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

```
pip install -r requirements.txt
```
At the bottom of Bob, click **Select Interpreter** and choose the one with `.venv` in it.

## STEP 6: Create the demo pull request
```
python setup_demo.py
```
You should see **"Done! Two branches created"**.

What happened: the project now has the shop's normal code (`main`) plus a teammate's
new code waiting for review (a **pull request**). That new code has 11 hidden problems.

Try it:
```
python -m reviewsquad prepare
```
```
python -m reviewsquad checks before
```
You'll see **8/8 tests passed**, but also many warnings. The tests pass, yet the code is
dangerous. That's the problem ReviewSquad solves.

## STEP 7: Add the ReviewSquad modes to Bob
ReviewSquad uses 6 Bob modes: **Review Lead**, **Security Reviewer**, **Bugs & Logic Reviewer**,
**Test Reviewer**, **Team Rules Reviewer**, and **Fixer**.

1. Open the Bob chat panel and click the **mode selector** (the dropdown that shows the
   current mode, like "Code" or "Agent").
2. If you already see **Review Lead** in the list, go to Step 8.
3. If not, create them by hand:
   - In Bob's mode settings, choose **create a new mode**.
   - Open `bob_modes/1_review_lead.md` in Bob.
   - Copy the **name**, the **Role definition** text, and the **Instructions** text into the matching boxes.
   - Allow the tools listed under **Allowed tools** (read / edit / command).
   - Save. Do the same for files 2 to 6.
   - Tip: the hackathon guide or Bob's help pages ("custom modes") show where this setting is.
4. Also paste the text from `.bob/rules/reviewsquad.md` into Bob's **rules / custom instructions**,
   if Bob doesn't load it automatically.

## STEP 8: Measure how long a human review takes
This number proves your impact to the judges, so be honest.
1. Open the files in `sample_app/store/` and try to review the new code yourself using
   `team_docs/CornerShop_Code_Review_Guidelines.pdf`. Time yourself, or ask a friend who codes.
2. Save your time (for example 60 minutes):
   ```
   python -m reviewsquad baseline 60
   ```
⚠ Don't open the `benchmark` folder in Bob. It contains the answers.

## STEP 9: Run the review with Bob (this is your demo!) 🎬
1. Start screen recording now (see Step 12) so you capture it.
2. In the Bob chat, pick the **Review Lead** mode.
3. Type:
   > Review this pull request.
4. Watch: Bob reads the guidelines PDF, then starts **4 reviewers at the same time**.
   If Bob asks to run a command, click **Approve** or **Run**.
5. Bob shows the verdict and asks *"Shall the Fixer fix these findings?"* Type **yes**.
6. At the end, open the report: right-click `docs/index.html` → **Reveal in File Explorer** → double-click it.
7. 📸 **Take screenshots of the Bob task session summary.** Every team member needs their own.
   Save them in a folder called `bob_screenshots`.

**Want to practise again?** Type this and answer `yes`:
```
python -m reviewsquad reset
```
(Only use it for practice. It erases the review.)

## STEP 10: Upload to GitHub
1. Make an account at **github.com**.
2. Click **+ → New repository**. Name: `reviewsquad`. Choose **Public**. Click **Create repository**.
3. In the terminal (change YOUR-NAME to your GitHub username):
   ```
   git add -A
   ```
   ```
   git commit -m "ReviewSquad review and fixes by IBM Bob"
   ```
   ```
   git remote add origin https://github.com/YOUR-NAME/reviewsquad.git
   ```
   ```
   git push -u origin --all
   ```
   ```
   git push origin --tags
   ```
   A GitHub login window may appear. Log in.
4. Check on GitHub that you can see the files.

## STEP 11: Put the report online (your Application URL)
1. On your GitHub repo page: **Settings → Pages**.
2. Source: **Deploy from a branch**. Branch: **feature/coupons-and-admin-login**, folder **/docs**. Click **Save**.
3. Wait 2 minutes. Your link is `https://YOUR-NAME.github.io/reviewsquad/`
   This is your **Application URL**.

## STEP 12: Video, texts and submission
- **Record:** use OBS Studio (free, obsproject.com) or the Windows **Snipping Tool → Record**.
- **Script:** follow `submission/video_script.md`. Keep the video under 3 minutes.
- **Texts:** copy them from the `submission/` folder into the form.
  In `bob_usage_statement.md`, fill the [brackets] with what really happened.
- **Cover image:** a screenshot of the top of your report page.

### Final checklist
- [ ] Repo is public, with no passwords or keys
- [ ] Bob screenshots from every team member
- [ ] Report link works
- [ ] Video under 3 minutes, showing Bob working for at least 90 seconds
- [ ] Both texts under 500 words
