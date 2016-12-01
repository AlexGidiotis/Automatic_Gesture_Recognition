clear
clc

path = '/media/dimitris/TOSHIBA EXT/Chalearn_GestureReco/Test_SKData_mat/';
files = dir('C:/Users/Alex/Documents/University/Python/Data/Test_SKData_mat/*.mat');
%files = dir('/media/dimitris/TOSHIBA EXT/Chalearn_GestureReco/Test_SKData_mat/*.mat');

for file = files'
    in_file = sprintf('C:/Users/Alex/Documents/University/Python/Data/Test_SKData_mat/%s',file.name);
    load(in_file);

    frames = Video.Frames;

    leftHandX = zeros(length(frames(1,:)),4);
    leftHandY = zeros(length(frames(1,:)),4);
    rightHandX = zeros(length(frames(1,:)),4);
    rightHandY = zeros(length(frames(1,:)),4);

    for i=1:length(frames(1,:))
        sk = frames(i).Skeleton;
        hipCenterX(i) = sk.PixelPosition(1,1);
        hipCenterY(i) = sk.PixelPosition(1,2);
        shoulderCenterX(i) = sk.PixelPosition(3,1);
        shoulderCenterY(i) = sk.PixelPosition(3,2);
        leftHandX(i,:) = sk.PixelPosition(5:8,1);
        leftHandY(i,:) = sk.PixelPosition(5:8,2);
        rightHandX(i,:) = sk.PixelPosition(9:12,1);
        rightHandY(i,:) = sk.PixelPosition(9:12,2);
    end    
    
    outName = file.name(1:12)
    fname = sprintf('C:/Users/Alex/Documents/University/Python/Data/Test_SKData_txt/%sSKData.txt',outName);
    fileID = fopen(fname,'w');

    for i=1:length(frames(1,:))
        fprintf(fileID,'Frame: %d ', i);
        
        fprintf(fileID,'Hip: %d,%d ', hipCenterX(i),hipCenterY(i));
        fprintf(fileID,'Shoulder_Center: %d,%d ', shoulderCenterX(i),shoulderCenterY(i));
        fprintf(fileID,'Left: %d,%d %d,%d %d,%d %d,%d ', leftHandX(i,1),leftHandY(i,1),...
        leftHandX(i,2),leftHandY(i,2),...
        leftHandX(i,3),leftHandY(i,3),...
        leftHandX(i,4),leftHandY(i,4));
        fprintf(fileID,'Right: %d,%d %d,%d %d,%d %d,%d\n', rightHandX(i,1),rightHandY(i,1),...
        rightHandX(i,2),rightHandY(i,2),...
        rightHandX(i,3),rightHandY(i,3),...
        rightHandX(i,4),rightHandY(i,4));
        
    end

    fclose(fileID);
end