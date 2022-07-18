import os
import re

def recursive_list_file(path, extension):
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                result.append(os.path.join(root, file))
    return result

def fix_content(content):
    # fix /cite
    content = re.sub(r"([a-zA-Z])[ ]*(\\cite)", r"\1~\2", content)
    content = re.sub(r"([a-zA-Z])[ ]*(\\ref)", r"\1~\2", content)

    # fix words
    content = re.sub(r"(map[ -]?point)", "map-point", content)
    content = re.sub(r"(re[ -]?projection)", "re-projection", content)

    # fix :
    content = re.sub(r"([a-zA-Z])[ ]?[:]", r"\1:", content)
    content = content.replace("~:", ":")

    content = content.replace("\\mappoint{}", "map-point")
    content = content.replace("\\Mappoint{}", "map-point")
    content = content.replace("\\mappoints{}", "map-points")
    content = content.replace("\\Mappoints{}", "map-points")

    content = content.replace("\\covisible{}", "covisible")
    content = content.replace("\\Covisible{}", "Covisible")
    content = content.replace("\\covisibles{}", "covisibles")
    content = content.replace("\\Covisibles{}", "Covisibles")

    content = content.replace("\\mapgroup{}", "tag")
    content = content.replace("\\Mapgroup{}", "Tag")
    content = content.replace("\\mapgroups{}", "tags")
    content = content.replace("\\Mapgroups{}", "Tags")

    content = content.replace("\\mapapp{}", "function")
    content = content.replace("\\Mapapp{}", "Function")
    content = content.replace("\\mapapps{}", "functions")
    content = content.replace("\\Mapapps{}", "Functions")

    content = content.replace("\\mappoint", "map-point")
    content = content.replace("\\Mappoint", "map-point")
    content = content.replace("\\mappoints", "map-points")
    content = content.replace("\\Mappoints", "map-points")

    content = content.replace("\\covisible", "covisible")
    content = content.replace("\\Covisible", "Covisible")
    content = content.replace("\\covisibles", "covisibles")
    content = content.replace("\\Covisibles", "Covisibles")

    content = content.replace("\\mapgroup", "tag")
    content = content.replace("\\Mapgroup", "Tag")
    content = content.replace("\\mapgroups", "tags")
    content = content.replace("\\Mapgroups", "Tags")

    content = content.replace("\\mapapp", "function")
    content = content.replace("\\Mapapp", "Function")
    content = content.replace("\\mapapps", "functions")
    content = content.replace("\\Mapapps", "Functions")

    return content

def main(project_id):
    os.system("git clone https://git.overleaf.com/" + project_id)

    all_tex_files = recursive_list_file(project_id, ".tex")

    for tex_file in all_tex_files:
        f = open(tex_file, "r")
        content = f.read()
        f.close()

        # fix /cite
        content = fix_content(content)

        # count the world "will"
        num_will = content.count("will")
        if num_will > 0:
            print("{} has {} 'will'".format(tex_file, num_will))

        f = open(tex_file, "w")
        f.write(content)
        f.close()

    # Ask for confirmation
    print("\n\n")
    print("The following files will be modified:")
    for tex_file in all_tex_files:
        print(tex_file)
    print("\n")
    print("Are you sure you want to continue? (y/n)")
    answer = input()
    if answer != "y":
        print("Aborted.")
        return

    os.chdir(project_id)
    os.system("git commit -a -m \"Automatic commit\"")
    os.system("git push")

if __name__ == '__main__':
    # ask for project id
    print("Please enter the project id:")
    project_id = input()
    main(project_id)

