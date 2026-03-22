import matplotlib.pyplot as plt
import matplotlib as mpl

def get_all_mpl_cmaps_dict(n_samples=5):
    all_cmaps = {}    
    #cmap_names = [name for name in mpl.colormaps if not name.endswith('_r')] 
    discrete = {'Pastel1':9, 'Pastel2':8, 'Paired':12, 'Accent':8, 'Dark2':8, 'Set1': 9, 'Set2':8, 'Set3':12, 'tab10':10, 'tab20':20, 'tab20b':20, 'tab20c':20}
    cmap_names = discrete.keys()
    for name in cmap_names:
        n_samples = discrete[name]
        cmap = plt.get_cmap(name)
        samples = [i/(n_samples-1) for i in range(n_samples)]        
        rgb_list = []
        for s in samples:
            r, g, b, _ = cmap(s)
            rgb_list.append((round(r, 4), round(g, 4), round(b, 4)))            
        all_cmaps[name] = rgb_list        
    return all_cmaps

master_dict = get_all_mpl_cmaps_dict(n_samples=64)

for name, colors in master_dict.items():
    cls = []
    for r, g, b in colors:
        cls.append(f"({r}, {g}, {b})")
    output = f"\t\'{name}\':\t [{', '.join(cls)}],"
    print(output)