cd ..\Device\EcoBT\Components
dir /s /b *.h > ..\..\..\code_parser\head_path.txt
cd ..\Project\ble\Profiles
dir /s /b *.h >> ..\..\..\..\..\code_parser\head_path.txt
cd ..\CodeGenerator\Source
dir /s /b *.h >> ..\..\..\..\..\..\code_parser\head_path.txt


cd ..\..\..\..\..\..\code_parser\src
python -i caterpillar.py
cd ..\
