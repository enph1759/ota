from src.video import video as vid
from src.pupil import pupil
from src.iris import iris
from src.data import data as dat

def construct_pupil_list(video, first_frame, last_frame):
    '''
    Construct a dictionary of pupil objects for a series of vide frames.

    Inputs:
        video - video object
        first_frame - int
        last_frame - int

    Outputs:
        pupil_list: Dictionary of pupil objects where the key is the frame number and the value is the pupil object.
    '''

    pupil_list = {}

    for i,frame in enumerate(video[first_frame:last_frame]):
        frame_loc = i + first_frame
        try:
            pupil_i = pupil.Pupil(frame)
        except pupil.EmptyAreas:
            print('Pupil not found in frame: %d \n None type object used inplace' % frame_index_list[idx])
            pupil_list[frame_loc] = None
        else:
            pupil_list[frame_loc] = pupil_i

    return pupil_list
