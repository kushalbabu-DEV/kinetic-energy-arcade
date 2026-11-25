# Publishing Kinetic Energy Arcade

The project is a Streamlit web application. Its entry point is:

`Kinetic_Energy_Arcade_COMPLETE/app.py`

## Existing Streamlit Community Cloud deployment

If this repository already has a deployed app, keep the existing deployment and main-file path. Push changes to the branch connected to Streamlit Community Cloud; the app should rebuild from the updated commit.

## Create a new deployment

1. Push the project to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Select **Create app** and choose this repository and the `main` branch.
4. Enter `Kinetic_Energy_Arcade_COMPLETE/app.py` as the main file path.
5. Deploy. Dependencies are read from `Kinetic_Energy_Arcade_COMPLETE/requirements.txt`.

## Test locally before publishing

From the project folder:

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

Then open `http://localhost:8501`.

## Update the repository from Windows

From the repository root:

```powershell
git status
git add Kinetic_Energy_Arcade_COMPLETE
git commit -m "Upgrade Kinetic Energy Arcade to version 2.0"
git push
```

Keep the folder name `Kinetic_Energy_Arcade_COMPLETE` unchanged. Do not create another nested copy of the project folder.

## If deployment fails

- Confirm the main file path is `Kinetic_Energy_Arcade_COMPLETE/app.py`.
- Check that `requirements.txt` is in the same project folder as `app.py`.
- Open the app's Streamlit Cloud dashboard and inspect the latest deployment logs.
- Run the app locally using the commands above to separate code issues from deployment configuration issues.
