"""Print a real charge from the recorded workspace's checkout implementation."""
import pathlib,sys
root=pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0,str(root/'.local/checkout-recording/workspace'))
from checkout import total
print('Cart: $50.00 | Coupon: 10%')
print('Charged: $%.2f' % (total(5000,10)/100))
