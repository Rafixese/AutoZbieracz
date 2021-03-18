var settings = {
max_ressources: '99999',
archers: '0',
skip_level_1: '0'
};

var settings_spear = {
untouchable: '0',
max_unit_number: '9999',
conditional_safeguard: '0'
};

var settings_sword = {
untouchable: '0',
max_unit_number: '9999',
conditional_safeguard: '0'
};

var settings_axe = {
untouchable: '0',
max_unit_number: '9999',
conditional_safeguard: '0'
};

var settings_archer = {
untouchable: '0',
max_unit_number: '9999',
conditional_safeguard: '0'
};

var settings_light = {
untouchable: '0',
max_unit_number: '9999',
conditional_safeguard: '0'
};

var settings_marcher = {
untouchable: '0',
max_unit_number: '9999',
conditional_safeguard: '0'
};

var settings_heavy = {
untouchable: '0',
max_unit_number: '9999',
conditional_safeguard: '0'
};

function fill(unit, number) {
	let field = $(`[name=${unit}]`);
	number = Number(number);
	field.trigger('focus');
	field.trigger('keydown');
	field.val(number);
	field.trigger('keyup');
	field.trigger('change');
	field.blur();
}
var units_settings = {
	0: settings_spear,
	1: settings_sword,
	2: settings_axe,
	3: settings_archer,
	4: settings_light,
	5: settings_marcher,
	6: settings_heavy
};

var units = {
	0: 'spear',
	1: 'sword',
	2: 'axe',
	3: 'archer',
	4: 'light',
	5: 'marcher',
	6: 'heavy'
};

var units_capacity = [25,15,10,10,80,50,50];
var to_send = [0,0,0,0,0,0,0];

var doc=document;
url=doc.URL;
if(url.indexOf('screen=place')==-1 || url.indexOf('mode=scavenge')==-1)
	alert('Skrypt do uzycia w placu w zakladce zbieractwo');
else{
	var unfree_levels = doc.getElementsByClassName('btn btn-default free_send_button btn-disabled');
	var unlocked_levels = doc.getElementsByClassName('btn btn-default free_send_button');
	var free_levels = unlocked_levels.length - unfree_levels.length;

	if(free_levels == 0)
		alert('Brak dostepnych poziomow zbieractwa');
	else{
		if(unlocked_levels.length > 1 && free_levels == 1 && settings.skip_level_1 == 1)
			alert('Ustawiono pominiecie 1 poziomu zbieractwa');
		else{
			let unit;
			for(var i = 0; i<7; i++){
				if(settings.archers == 0)
					if(i==3 || i==5)
						i++;
				if(units_settings[i].max_unit_number > 0){
					unit = units[i];
					let field = $(`[name=${unit}]`)
					let available = Number(field[0].parentNode.children[1].innerText.match(/\d+/)[0]);

					if(available > units_settings[i].untouchable)
						available -= units_settings[i].untouchable;
					else
						available = 0;

					if(available >= units_settings[i].conditional_safeguard)
						available -= units_settings[i].conditional_safeguard;

					if(unlocked_levels.length == 1){
						if(available > units_settings[i].max_unit_number)
							available = units_settings[i].max_unit_number;
						to_send[i] = available;
					}
					else{
						let packs = 0;
						if(settings.skip_level_1 == 0)
							packs += 15;
						if(unlocked_levels.length >= 2)
							packs += 6;
						if(unlocked_levels.length >= 3)
							packs += 3;
						if(unlocked_levels.length == 4)
							packs += 2;

						let left_packs = 0;
						let packs_now;

						if(free_levels >= 1 && settings.skip_level_1 == 0){
							packs_now = 15;
							left_packs += 15;
						}
						if(free_levels >= 2){
							packs_now = 6;
							left_packs += 6;
						}
						if(free_levels >= 3){
							packs_now = 3;
							left_packs += 3;
						}
						if(free_levels ==4){
							packs_now = 2;
							left_packs += 2;
						}

						if(available*packs/left_packs > units_settings[i].max_unit_number)
							to_send[i] = units_settings[i].max_unit_number*packs_now/packs;
						else
							to_send[i] = available*packs_now/left_packs;
					}
				}
			}

			let capacity = 0;
			for(var i = 0; i<7; i++){
				if(settings.archers == 0)
					if(i==3 || i==5)
						i++;
				capacity += units_capacity[i] * to_send[i];
			}

			if(free_levels == 1){
				settings.max_ressources *= 10;
			}
			else if(free_levels == 2){
				settings.max_ressources *= 4;
			}
			else if(free_levels == 3){
				settings.max_ressources *= 2;
			}
			else{
				settings.max_ressources *= 1.3333;
			}

			if(capacity > settings.max_ressources){
				let ratio = settings.max_ressources / capacity;
				for(var i = 0; i<7; i++){
					if(settings.archers == 0)
						if(i==3 || i==5)
							i++;
					to_send[i] = to_send[i] * ratio;
				}
			}

			for(var i = 0; i<7; i++){
				if(settings.archers == 0)
					if(i==3 || i==5)
						i++;
				unit = units[i];
				fill(unit, Math.floor(to_send[i]));
			}
		}
	}
}
void(0);