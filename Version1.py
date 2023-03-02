import instaloader
import os
import shutil

while True:
    L = instaloader.Instaloader()

    profile = input("Enter the profile name (make sure it's public and correct): ")

    try:
        profile_obj = instaloader.Profile.from_username(L.context, profile)
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile '{profile}' does not exist.")
        run_again = input("Do you want to run the program again? (y/n) ")
        if run_again.lower() == 'n':
            break
        else:
            continue

    if profile_obj.is_private:
        print(f"Profile '{profile}' is private.")
        run_again = input("Do you want to run the program again? (y/n) ")
        if run_again.lower() == 'n':
            break
        else:
            continue

    num_posts = profile_obj.mediacount 
    batch_size = input(f"Enter the batch size (the amount of posts per folder, not over {num_posts}): ")

    try:
        batch_size = int(batch_size)
        if batch_size > num_posts:
            print(f"Invalid batch size, please enter a number (not over {num_posts}).")
            run_again = input("Do you want to run the program again? (y/n) ")
            if run_again.lower() == 'n':
                break
            else:
                continue
    except ValueError:
        print(f"Invalid batch size, please enter a number (not over {num_posts}).")
        run_again = input("Do you want to run the program again? (y/n) ")
        if run_again.lower() == 'n':
            break
        else:
            continue


    L.download_profile(profile, profile_pic_only=False)

    directory = "./" + profile
    if not os.path.exists(directory):
        os.mkdir(directory)

    batch_count = 1
    batch_directory = None
    batch_post_count = 0

    metadata_directory = os.path.join(directory, "Metadata")
    if not os.path.exists(metadata_directory):
        os.mkdir(metadata_directory)

    for count, filename in enumerate(sorted(os.listdir(directory))):
        if filename.endswith(".jpg") or filename.endswith(".mp4"):
            if batch_post_count == 0:
                batch_directory = os.path.join(directory, f"Batch_{batch_count}")
                if not os.path.exists(batch_directory):
                    os.mkdir(batch_directory)
            target_file = os.path.join(batch_directory, filename)
            if os.path.exists(target_file):
                name, ext = os.path.splitext(filename)
                i = 1
                while os.path.exists(os.path.join(batch_directory, f"{name}_{i}{ext}")):
                    i += 1
                target_file = os.path.join(batch_directory, f"{name}_{i}{ext}")
            os.rename(os.path.join(directory, filename), target_file)
            caption_filename = os.path.splitext(filename)[0] + ".txt"
            if os.path.exists(os.path.join(directory, caption_filename)):
                os.rename(os.path.join(directory, caption_filename), os.path.join(batch_directory, caption_filename))
            batch_post_count += 1
            if batch_post_count == batch_size:
                batch_count += 1
                batch_post_count = 0
        elif filename.endswith(".json.xz"):
            os.rename(os.path.join(directory, filename), os.path.join(metadata_directory, filename))

    shutil.make_archive(profile, 'zip', directory)

    run_again = input("Do you want to run the program again? (y/n) ")
    if run_again.lower() == 'n':
        break
