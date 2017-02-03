clear
clc

files = dir('/media/dimitris/TOSHIBA EXT/Chalearn_GestureReco/Test_SKData_mat/*.mat');
%files = dir('C:/Users/Alex/Documents/University/Python/Data/Test_SKData_mat/*.mat')

for file = files'
    %in_file = sprintf('C:/Users/Alex/Documents/University/Python/Data/Test_SKData_mat/%s',file.name);
    in_file = sprintf('/media/dimitris/TOSHIBA EXT/Chalearn_GestureReco/Test_SKData_mat/%s',file.name);

    %file.name
    load(in_file)
    Video
    labels = Video.Labels;
    
    outName = file.name(1:16);
    %fname = sprintf('C:/Users/Alex/Documents/University/Python/Data/Test_Labels/%s_labels.txt',outName);
    fname = sprintf('/home/dimitris/GitProjects/Automatic_Gesture_Recognition/Test_Labels/%s_labels.txt',outName);

    fileID = fopen(fname,'w');

    for i=1:length(labels(1,:))     
        fprintf(fileID,'%s Begin: %d End: %d\n',labels(i).Name,labels(i).Begin,labels(i).End);
    end

    fclose(fileID);
end