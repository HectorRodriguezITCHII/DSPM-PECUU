import urllib.request
import socket
import sys

class NetworkScanner:
    def __init__(self, wan_url='https://api.ipify.org'):
        self.lan_ip = self.get_lan_ip()
        self.wan_ip = self.get_wan_ip(wan_url)
        self.default_ports = [80, 81, 82, 554, 1024, 1025]
    
    def get_lan_ip(self):
        """Obtiene la IP local (LAN)"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    
    def get_wan_ip(self, wan_url):
        """Obtiene la IP pública (WAN)"""
        try:
            wan_ip = urllib.request.urlopen(wan_url).read().decode('utf8')
            return wan_ip
        except Exception as e:
            print(f"Error al obtener la IP pública: {e}")
            return None
    
    def scan_ports(self, target_ip=None, port_list=None):
        """Escanea los puertos de una IP específica"""
        if target_ip is None:
            target_ip = self.wan_ip
        
        if port_list is None:
            port_list = self.default_ports
            
        print(f"\nIniciando escaneo de puertos para: {target_ip}")
        print("=" * 50)
        
        for port in port_list:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                status = sock.connect_ex((target_ip, port))
                
                if status == 0:
                    print(f"Puerto {port}: \t ABIERTO")
                else:
                    print(f"Puerto {port}: \t CERRADO")
                    
                sock.close()
            except socket.error as err:
                print(f"Error de conexión en puerto {port}: {err}")
                sock.close()
            except KeyboardInterrupt:
                print("\nEscaneo interrumpido por el usuario.")
                sys.exit()

def main():
    # Crear instancia del scanner
    scanner = NetworkScanner()
    
    # Mostrar IPs
    print("\nInformación de red:")
    print("=" * 50)
    print(f"IP Local (LAN): {scanner.lan_ip}")
    print(f"IP Pública (WAN): {scanner.wan_ip}")
    
    # Preguntar al usuario qué IP quiere escanear
    print("\nOpciones de escaneo:")
    print("1. Escanear mi IP pública")
    print("2. Escanear otra IP")
    
    opcion = input("\nSeleccione una opción (1/2): ")
    
    if opcion == "1":
        scanner.scan_ports()
    elif opcion == "2":
        ip_objetivo = input("Ingrese la IP a escanear: ")
        scanner.scan_ports(ip_objetivo)
    else:
        print("Opción no válida")

if __name__ == "__main__":
    main()