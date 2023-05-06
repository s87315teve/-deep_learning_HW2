with open("aishell_transcript_origin.txt", "r") as file_old:
    with  open("aishell_transcript.txt", "w") as file_new:
        line=file_old.readline()
        file_new.write(line)
        line=file_old.readline()
        while line:
            if line!="":
                file_new.write(line)
                file_new.write("a"+line)
                line=file_old.readline()

