clear
clc

files = dir('C:/Users/Alex/Documents/University/Python/Data/SKData_mat/*.mat');

for file = files'
    in_file = sprintf('C:/Users/Alex/Documents/University/Python/Data/SKData_mat/%s',file.name);
    
    load(in_file)

    labels = Video.Labels;
    
    outName = file.name(1:16);
    fname = sprintf('C:/Users/Alex/Documents/University/Python/Data/Labels/%s_labels.txt',outName);
    fileID = fopen(fname,'w');

    for i=1:length(labels(1,:))     
        fprintf(fileID,'%s Begin: %d End: %d\n',labels(i).Name,labels(i).Begin,labels(i).End);
    end

    fclose(fileID);
end