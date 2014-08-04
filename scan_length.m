clear all;clear classes

params = struct('resolution',128,'grid_size',400e-6,'input_waist',23E-6, 'CA_pilier', 0.025, ...
    'CA_roc', 350E-6, 'transmission',200E-6,'roc_depth',800E-9, 'w_m', (44.7E-6)^2)
id=19;

addpath(genpath('D:\drive\Soft\OscarV3.14\Classes'));
addpath('jsonlab');

data_path = 'D:\drive\Theorie\OscarSimu\data'
script_backup_path = 'D:\drive\Theorie\OscarSimu\scripts'

FileNameAndLocation=[mfilename('fullpath')];
[pathstr,name,ext] = fileparts(FileNameAndLocation)
new_name = sprintf('%s_%04i.m', name, id);
newbackup = fullfile(script_backup_path,new_name)
currentfile=strcat(FileNameAndLocation, '.m');
data_name = sprintf('%s/%04i_losses_of_l.csv', data_path, id)
json_name = sprintf('%s/%04i_losses_of_l.json', data_path, id)
if exist(data_name)
    err = MException('AcctError:Incomplete','id already exist')
    throw(err)
end
copyfile(currentfile, newbackup);

disp('---------------------------------------------------------------------------')
disp('                  OSCAR V3.14                                      ')
disp('  ')


% Define the grid for the simulation
G1 = Grid(params.resolution, params.grid_size);

% Define the incoming beam on the input mirror surface
E_input = E_Field(G1,'w0',params.input_waist);

% Define the cavity mirror
L18 = Interface(G1,'RoC',inf,'CA',params.CA_pilier,'T',0);         
uRoC = Interface(G1,'RoC',inf,'CA',params.CA_roc,'T',params.transmission);           % Clear diameter 130 um

% Create a Gaussian surface
uRoC.surface = params.roc_depth*exp(-2*G1.D2_square /params.w_m);

length_start = 100e-6
length_end = 1000e-6
n_points = 100
step_length = (length_end - length_start)/n_points
losses = zeros(1,n_points);
index = 1;
lengths = length_start:step_length:length_end
for length=lengths,
    % Use the 2 previous Interfaces and the input beam to define a cavity 
    fprintf('calcuating %f mum', length)
    C1 = Cavity1(uRoC, L18, length,E_input);
    C1.Laser_start_on_input = false;

    % Check the cavity parameters
    C1.Check_stability();

    % Calculate the resonance length
    C1 = Cavity_resonance_phase(C1);


    % Calculate the resonance length
    %C1 = Cavity_scan(C1);

    % Display information about the cavity
    % Display_scan(C1);

     % Display information about the cavity
    [field,RTL] = Get_info_AC(C1);
    losses(index) = RTL;
    index = index+1;
end
%C1 = Calculate_fields(C1);
%Display_results(C1);
hold on
semilogy(lengths, losses)
csvwrite(data_name,[lengths; losses])

to_json = savejson('params', params)

fileID = fopen(json_name,'w');
fprintf(fileID,to_json);
fclose(fileID);