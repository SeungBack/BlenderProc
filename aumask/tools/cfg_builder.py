import random

def initialize_cfg(output_dir, config_path):
    return {
    "version": 3,
    "setup": {
      "blender_install_path": "/home_local/<env:USER>/blender/",
      "pip": [
        "h5py",
        "pypng==0.0.20",
      ]
    },
    "modules": [
      {
        "module": "main.Initializer",
        "config": {
            "global": {
            "output_dir": output_dir,
            "sys_paths": [config_path],            
          }
        }
      }
    ]
    }

def build_bin_loader(opt):

    asset_conditions = []
    for asset in opt["bin"]["texture_assets"]:
      asset_conditions.append({"name": "{}*".format(asset)})
    X = random.uniform(opt["bin"]["size"]["X"]["min"], opt["bin"]["size"]["X"]["max"])
    Y = random.uniform(opt["bin"]["size"]["Y"]["min"], opt["bin"]["size"]["Y"]["max"])
    Z = random.uniform(opt["bin"]["size"]["Z"]["min"], opt["bin"]["size"]["Z"]["max"])
    thickness = random.uniform(opt["bin"]["size"]["thickness"]["min"], opt["bin"]["size"]["thickness"]["max"])
    return [
    {
      "module": "constructor.BasicMeshInitializer",
      "config": {
        "meshes_to_add": [
        {
          "type": "cube",
          "name": "bin_cube1",
          "location": [0, 0, 0],
          "scale": [X, Y, thickness],
        },
        {
          "type": "cube",
          "name": "bin_cube2",
          "location": [-X, 0, Z/2],
          "scale": [thickness, Y + thickness, Z/2],
        },
        {
          "type": "cube",
          "name": "bin_cube3",
          "location": [X, 0, Z/2],
          "scale": [thickness, Y + thickness, Z/2],
        },
        {
          "type": "cube",
          "name": "bin_cube4",
          "location": [0, -Y, Z/2],
          "scale": [X, thickness, Z/2],
        },
        {
          "type": "cube",
          "name": "bin_cube5",
          "location": [0, Y, Z/2],
          "scale": [X, thickness, Z/2],
        }
        ]
      }
    },
    {
      "module": "manipulators.EntityManipulator",
      "config": {
        "selector": {
          "provider": "getter.Entity",
          "conditions": {
            "name": '.*cube.*'
          }
        },
        "cp_physics": False,
        "cp_category_id": 255        
      }
    },
    {
      "module": "loader.CCMaterialLoader",
      "config": {
        "folder_path": opt["cctexture_path"],
        "used_assets": opt["bin"]["texture_assets"]
      }
    },
    {
      "module": "manipulators.EntityManipulator",
      "config": {
        "selector": {
          "provider": "getter.Entity",
          "conditions": {
          "name": "bin_cube.*"
          }
        },
        "mode": "once_for_all",
        "cf_randomize_materials": {
          "randomization_level": 1,
          "materials_to_replace_with": {
            "provider": "getter.Material",
            "conditions": asset_conditions,
            "random_samples": 1,
            "conditions": [{
              "cp_is_cc_texture": True
            }
        ]}
        }
      }
      },
    {
    "module": "manipulators.MaterialManipulator",
    "config": {
      "selector": {
        "provider": "getter.Material",
        "conditions": {
        "name": "bin_cube.*"
        }
      },
      "mode": "once_for_all",
      "cf_set_base_color": {
        "provider": "sampler.Color",
        "min": [0.1, 0.1, 0.1, 1.0],
        "max": [0.9, 0.9, 0.9, 1.0]
      },
      "cf_set_specular": {
            "provider": "sampler.Value",
            "type": "float",
            "min": 0.0,
            "max": 1.0
        },
        "cf_set_roughness": {
            "provider": "sampler.Value",
            "type": "float",
            "min": 0.0,
            "max": 1.0
        }
    }
    }
    ]

def build_plane_loader(opt):
    asset_conditions = []
    for asset in opt["table_texture_assets"]:
      asset_conditions.append({"name": "{}*".format(asset)})
    return [
    {
      "module": "constructor.BasicMeshInitializer",
      "config": {
        "meshes_to_add": [
        {
          "type": "plane",
          "name": "ground_plane0",
          "scale": [2, 2, 1]
        },
        {
          "type": "plane",
          "name": "ground_plane1",
          "scale": [2, 2, 1],
          "location": [0, -2, 2],
          "rotation": [-1.570796, 0, 0] # switch the sign to turn the normals to the outside
        },
        {
          "type": "plane",
          "name": "ground_plane2",
          "scale": [2, 2, 1],
          "location": [0, 2, 2],
          "rotation": [1.570796, 0, 0]
        },
        {
          "type": "plane",
          "name": "ground_plane4",
          "scale": [2, 2, 1],
          "location": [2, 0, 2],
          "rotation": [0, -1.570796, 0]
        },
        {
          "type": "plane",
          "name": "ground_plane5",
          "scale": [2, 2, 1],
          "location": [-2, 0, 2],
          "rotation": [0, 1.570796, 0]
        },
        {
          "type": "plane",
          "name": "light_plane",
          "location": [0, 0, 10],
          "scale": [3, 3, 1]
        }
        ]
      }
    },
    {
      "module": "manipulators.EntityManipulator",
      "config": {
        "selector": {
          "provider": "getter.Entity",
          "conditions": {
            "name": '.*plane.*'
          }
        },
        "cp_physics": False,
        "cp_category_id": 5000      
      }
    },
    {
      "module": "manipulators.MaterialManipulator",
      "config": {
        "selector": {
          "provider": "getter.Material",
          "conditions": {
            "name": "light_plane_material"
          }
        },
        "cf_switch_to_emission_shader": {
          "color": {
            "provider": "sampler.Color",
            "min": [0.5, 0.5, 0.5, 1.0],
            "max": [1.0, 1.0, 1.0, 1.0]
          },
          "strength": {
            "provider": "sampler.Value",
            "type": "float",
            "min": 3,
            "max": 6
          }
        }
      }
    },
    {
      "module": "loader.CCMaterialLoader",
      "config": {
        "folder_path": opt["cctexture_path"],
        "used_assets": opt["table_texture_assets"]
      }
    },
    {
      "module": "manipulators.EntityManipulator",
      "config": {
        "selector": {
          "provider": "getter.Entity",
          "conditions": {
            "name": "ground_plane.*"
          }
        },
        "cf_randomize_materials": {
          "randomization_level": 1,
          "materials_to_replace_with": {
            "provider": "getter.Material",
            "conditions": asset_conditions,
            "random_samples": 1,
            "conditions": [{
              "cp_is_cc_texture": True
            }
        ]}
        }
    }
    }
    ]

def build_object_loader(object_path, category_id):
    return [{
    "module": "loader.ObjectLoader",
    "config": {
      "path": object_path,
      "add_properties": {
          "cp_category_id": str(category_id),
          "cp_physics": True,
          "cp_scale": [0.001, 0.001, 0.001],
      }
    }
    },
  
    {
    "module": "manipulators.EntityManipulator",
    "config": {
      "selector": {
        "provider": "getter.Entity",
        "conditions": {
          "type": "MESH"  # this guarantees that the object is a mesh, and not for example a camera
        }
      },
      "scale": [0.001, 0.001, 0.001]
    }
    } 
    ]

def build_bop_loader(opt, dataset_name, num_of_objs_to_sample, obj_ids):
    upright = True if dataset_name == "kit" else False
    randomtexture = True if dataset_name == "3dnet" else False
    module = [{
      "module": "loader.BopLoader",
      "config": {
          "bop_dataset_path": "{}/{}".format(opt["bop_path"], dataset_name),
          "model_type": "",
          "mm2m": True,
          "obj_ids": obj_ids,
          "sample_objects": True,
          "num_of_objs_to_sample": num_of_objs_to_sample,
          "add_properties": {
          "cp_physics": True,
          "cp_upright": upright,
          "cp_randomtexture": randomtexture
          },
      }
    }]
    if dataset_name != "tless" and dataset_name != "itodd":
      module[0]["config"]["cf_set_shading"] = "SMOOTH"
    return module

def build_object_pose_sampler(opt,is_kit):
    module =[
     {
      "module": "object.ObjectPoseSampler",
      "config": {
        "objects_to_sample": {
          "provider": "getter.Entity",
          "conditions": {
            "cp_physics": True
          }
        },
        "pos_sampler": {
          "provider":"sampler.Uniform3d",
          "min": opt["object"]["position"]["min"],
          "max": opt["object"]["position"]["max"]
          },
        "rot_sampler":{
          "provider":"sampler.UniformSO3"
        }
        },
    },
    {
      "module": "object.PhysicsPositioning",
      "config": {
        "min_simulation_time": 3,
        "max_simulation_time": 10,
        "check_object_interval": 1,
        "solver_iters": 25,
        "substeps_per_frame": 20,
        "friction": 100.0,
        "linear_damping": 0.99,
        "angular_damping": 0.99,
        "objs_with_box_collision_shape": {
          "provider": "getter.Entity",
          "conditions": [{
            "type": "plane"
          },
          {
            "type": "cube"
          }
          ]
        }
      }
      }
      ]

    if is_kit:
      module.insert(1, {
      "module": "object.ObjectPoseSampler",
      "config": {
        "objects_to_sample": {
          "provider": "getter.Entity",
          "conditions": {
            "cp_upright": True
          }
        },
        "pos_sampler": {
          "provider":"sampler.Uniform3d",
          "min": opt["object"]["position"]["min"],
          "max": opt["object"]["position"]["max"]
          },
        "rot_sampler":{
          "provider":"sampler.UniformSO3",
          "around_x": False,
          "around_y": False,
          "around_z": True,
        }
        },
    })

    return module

def build_light_sampler(opt):

    energy = random.uniform(opt["light"]["energy"]["min"], opt["light"]["energy"]["max"])
    return [{
      "module": "lighting.LightSampler",
      "config": {
        "lights": [
        {
          "location": {
            "provider": "sampler.Shell",
            "center": opt["light"]["center"],
            "radius_min": opt["light"]["radius"]["min"],
            "radius_max": opt["light"]["radius"]["min"],
            "elevation_min": opt["light"]["elevation"]["min"],
            "elevation_max": opt["light"]["elevation"]["min"],
            "uniform_elevation": True
          },
          "color": {
            "provider": "sampler.Color",
            "min": opt["light"]["color"]["min"],
            "max": opt["light"]["color"]["max"]
          },
          "type": "POINT",
          "energy": energy
        }
        ]
      }
    },]

def build_camera_sampler(opt):
    module = [{
      "module": "camera.CameraSampler",
      "config": {
        "intrinsics": {
          "cam_K": opt["camera"]["cam_K"],
          "resolution_x": opt["camera"]["resolution"]["x"],
          "resolution_y": opt["camera"]["resolution"]["y"]
        },
        "cam_poses": [
        {  
          "proximity_checks": {
            "min": opt["camera"]["proximity_checks"]
          },
          "excluded_objs_in_proximity_check":  {
            "provider": "getter.Entity",
            "conditions": {
              "name": "ground_plane.*",
              "type": "MESH"
            }
          },
          "number_of_samples": opt["num_of_imgs_per_seq"],
          "location": {
            "provider": "sampler.Shell",
            "center": opt["camera"]["center"],
            "radius_min": opt["camera"]["radius"]["min"],
            "radius_max": opt["camera"]["radius"]["max"],
            "elevation_min": opt["camera"]["elevation"]["min"],
            "elevation_max": opt["camera"]["elevation"]["max"],
            "uniform_elevation": opt["camera"]["uniform_elevation"]
          }
          
        }
        ]
      }
    }]
    if opt["bin"]["is_used"]: 
      module[0]["config"]["cam_poses"][0]["rotation"] = {
            "format": "look_at",
            "value": [0, 0, 0],
            "inplane_rot": {
              "provider": "sampler.Value",
              "type": "float",
              "min": opt["camera"]["inplane_rot"]["min"],
              "max": opt["camera"]["inplane_rot"]["min"]
            }
        }
    else: 
      module[0]["config"]["cam_poses"][0]["rotation"] = {
      "format": "look_at",
      "value": {
            "provider": "getter.POI",
            "selector": {
              "provider": "getter.Entity",
              "conditions": {
                "type": "MESH",
              },
              "random_samples": opt["num_of_imgs_per_seq"]
            }
          },
          "inplane_rot": {
              "provider": "sampler.Value",
              "type": "float",
              "min": opt["camera"]["inplane_rot"]["min"],
              "max": opt["camera"]["inplane_rot"]["min"]
          }
        }     

    return module

def build_object_material_manipulator(opt):
    conditions = []
    for dataset_name in opt["dataset_names"]:
        conditions.append({"name": "bop_{}_vertex_col_matrial.*".format(dataset_name)})
    module = [
      {
        "module": "manipulators.MaterialManipulator",
        "config": {
          "selector": {
            "provider": "getter.Material",
            "conditions": {
              "name": "ply_material"
            }
          },
          "cf_change_to_vertex_color": "Col"
        }
      },
      {
        "module": "manipulators.MaterialManipulator",
        "config": {
        "mode": "once_for_each",
        "selector": {
            "provider": "getter.Material",
            "conditions": conditions
        },
        "cf_set_specular": {
            "provider": "sampler.Value",
            "type": "float",
            "min": 0.0,
            "max": 1.0
        },
        "cf_set_roughness": {
            "provider": "sampler.Value",
            "type": "float",
            "min": 0.0,
            "max": 1.0
        }
        }
      },
      {
        "module": "manipulators.MaterialManipulator",
        "config": {
          "mode": "once_for_each",
          "selector": {
            "provider": "getter.Material",
            "conditions": [
            {
              "name": "bop_tless_vertex_col_material.*"
            },
            {
              "name": "bop_itodd_vertex_col_material.*"
            }
            ]
          },
          "cf_set_base_color": {
            "provider": "sampler.Color",
            "grey": True,
            "min": [0.1, 0.1, 0.1, 1.0],
            "max": [0.9, 0.9, 0.9, 1.0]
          }
        }
      }
      ]
    if "3dnet" in opt["dataset_names"]:
        module.append( {
        "module": "loader.CCMaterialLoader",
        "config": {
          "folder_path": opt["cctexture_path"],
          # "used_assets": opt["table_texture_assets"]
        }
      },)
        module.append(
        {
        "module": "manipulators.EntityManipulator",
        "config": {
          "selector": {
            "provider": "getter.Entity",
            "conditions": {
              "cp_randomtexture": True
            }
          },
          "mode": "once_for_each",
          "cf_randomize_materials": {
            "randomization_level": 1,
            "materials_to_replace_with": {
              "provider": "getter.Material",
              "random_samples": 1,
              "conditions": [{
                "cp_is_cc_texture": True
              }
          ]}
          }
      }
      }
      )



    return module

def build_rgb_render(opt):
    return [{
      "module": "renderer.RgbRenderer",
      "config": {
        "samples": opt["num_of_imgs_per_seq"],
        "render_distance": True,
        "image_type": "PNG"
      }
    }]

def build_bop_writer(opt):
      
    return [{
      "module": "writer.BopWriter",
      "config": {
        "m2mm": True, # original bop annotations in mm (default)
        "append_to_existing_output": True,
        "postprocessing_modules": {
          "distance": [
            {"module": "postprocessing.Dist2Depth"}
          ]
        }
      }
    }]
