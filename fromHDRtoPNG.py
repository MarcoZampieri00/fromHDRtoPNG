import spectral as sp
import spectral.io.envi as envi
import os
import sys

def fromHDRtoPNG(file,min_wl=-1,max_wl=-1):

  header_file_path='images/'+file+'.hdr'
  print(header_file_path)

  if not os.path.isfile(header_file_path):
    raise ValueError("The file does not exist.")

  if not isinstance(min_wl, int) or min_wl < -1:
    raise ValueError("The minimum wavelength needs to be an integer greater or equal to -1.")

  if not isinstance(max_wl, int) or max_wl < -1:
    raise ValueError("The maximum wavelength needs to be an integer greater or equal to -1.")

  img = envi.open(header_file_path)
  header = envi.read_envi_header(header_file_path)

  wavelength=header['wavelength']
  
  nome_cartella = file+"_png"
  
  try:
    if not os.path.exists(nome_cartella):
      os.mkdir(nome_cartella)
    print(f"Cartella '{nome_cartella}' creata con successo.")
  except OSError as errore:
    print(f"Errore durante la creazione della cartella: {errore}")

  if min_wl==-1 and max_wl==-1:
    for i in range(len(wavelength)): #len(wavelength)
      band=img.read_band(i)
      filename=f"{nome_cartella}/{file}_wl_{wavelength[i]}.png"
      sp.save_rgb(filename,band,format='png')
  else:
    for i in range(len(wavelength)):
      if float(wavelength[i])>int(min_wl) and float(wavelength[i])<int(max_wl):
        band=img.read_band(i)
        filename=f"{nome_cartella}/{file}_wl_{wavelength[i]}.png"
        sp.save_rgb(filename,band,format='png')
        
def main():
    args = sys.argv[1:]  # Ignora il primo elemento, che è il nome dello script
    if len(args) != 3:
        print("Correct use: python3 fromHDRtoPNG.py <path_to_file> <min_wavelength> <max_wavelength>")
    else:
        filename=args[0]
        min_wl=int(args[1])
        max_wl=int(args[2])
        fromHDRtoPNG(filename,min_wl,max_wl)
    

if __name__ == "__main__":
    main()