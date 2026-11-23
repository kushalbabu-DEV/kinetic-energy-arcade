# Online deployment checklist

## Before deployment
- [ ] Run locally with `py -m streamlit run app.py`.
- [ ] Test all five menu options.
- [ ] Test the collision with Object A = 5 m/s and Object B = 0 m/s.
- [ ] Test the roller coaster at 0%, 50% and 100%.
- [ ] Confirm the `assets` folder is present.

## GitHub upload
Upload the contents of `Kinetic_Energy_Arcade_COMPLETE` to a GitHub repository:
- `app.py`
- `requirements.txt`
- `README.md`
- `assets/images/arcade_bolt.png`
- `assets/sounds/*.wav`

## Streamlit Community Cloud
1. Sign in to Streamlit Community Cloud using GitHub.
2. Select **Create app**.
3. Select the repository and `main` branch.
4. Set main file path to `app.py`.
5. Deploy.
6. Test the public URL in a private/incognito browser window.

The public website will run while the hosting service is available. Keep the GitHub repository as the source of truth for future updates.
