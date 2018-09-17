class RP:
    def __init__(self):
          self.width = 640
          self.height = 486
          self.gamma = 0
          self.theta = 0
          self.phi = 0
          self.alpha = 0
          self.t2d = [0,0]
          self.camera_pos = [0,0,3400]
          self.scale_scene = 0.0
          #rselfp.object_size  = 0.615 * 512
          self.shift_object = [0,0,-46125]
          #rp.shift_object = [0;0;0];
          self.shift_world = [0,0,0]
          self.scale = 0.001
          self.ac_g = [1,1,1]
          self.ac_c = 1
          self.ac_o = [0,0,0]
          #self.ambient_col  = 0.6*[1,1,1]
          #rp.rotm         = eye(3) ???
          self.use_rotm = 0
          self.do_remap = 0
          self.dir_light = []
          self.do_specular = 0.1
          self.phong_exp = 8
          self.specular = 0.1*255
          self.do_cast_shadows = 1
          self.sbufsize = 200
          # projection method
          self.proj = 'perspective'
          # if scale_scene == 0, then f is used:
          self.f = 6000
          # is 1 for grey level images and 3 for color images
          self.n_chan = 3
          self.backface_culling = 2; # 2 = default for current projection
          # can be 'phong', 'global_illum' or 'no_illum'
          #self.illum_method = 'phong'
          #self.global_illum.brdf = 'lambert'
          #self.global_illum.envmap = struct([])
          #self.global_illum.light_probe = []
          self.ablend = [] # no blending performed
