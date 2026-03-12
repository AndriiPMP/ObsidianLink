import os                                                          

def get_file_paths(directory):                                     
     file_paths = []                                                
     for root, directories, files in os.walk(directory):            
         for filename in files:                                     
             filepath = os.path.join(root, filename)                
             file_paths.append(filepath)                            
     return file_paths                                              
                                                                    
if __name__ == "__main__":                                         
    target_dir = r"E:\План\IT"                                     
                                                                    
    if os.path.exists(target_dir):                                 
        paths = get_file_paths(target_dir)                         
        for p in paths:                                            
            print(p)                                               
        print(f"\nНайдено файлов: {len(paths)}")                   
    else:                                                          
        print(f"Директория не найдена: {target_dir}")    