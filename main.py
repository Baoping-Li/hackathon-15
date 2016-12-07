import cloudstorage


def create_bucket(gcs):
    print "Create Bucket...."
    bucket_name = raw_input("Please enter bucket name: ")
    if gcs.create_bucket(bucket_name):
        print "Successfully created bucket or bucket already exists"


def upload_file(gcs):
    print "Upload file...."
    bucket_name, file_name = get_input()
    if gcs.store_file_to_gcs(bucket_name, file_name):
        print "Successfully uploaded file"


def download_file(gcs):
    print "Download file...."
    bucket_name, file_name = get_input()
    if gcs.fetch_object_from_gcs(bucket_name, file_name):
        print "Successfully downloaded file"


def list_bucket(gcs):
    print "List Bucket...."
    bucket_name = raw_input("Please enter bucket name: ")
    gcs.list_objects(bucket_name)


def get_input():
    bucket_name = raw_input("Please enter bucket name: ")
    file_name = raw_input("Please enter file name: ")
    return bucket_name, file_name


def menu():
    print ""
    print "Create a GCS Bucket       , enter 1"
    print "Store a file to GCS Bucket, enter 2"
    print "Fetch file from GCS Bucket, enter 3"
    print "List objects in GCS Bucket, enter 4"
    print "To Exit, enter 5"
    print ""
    try:
        selection = int(raw_input('Enter your selection: '))
        if selection > 5 or selection < 1:
            print "Error: please enter valid number"
            return menu()
        else:
            return selection
    except ValueError:
        print "Error: Please enter a number"
        return menu()


def main():
    gcs = cloudstorage.Storage()

    while True:
        selection = menu()

        if selection == 1:
            create_bucket(gcs)
        elif selection == 2:
            upload_file(gcs)
        elif selection == 3:
            download_file(gcs)
        elif selection == 4:
            list_bucket(gcs)
        else:
            break

if __name__ == '__main__':
    main()
