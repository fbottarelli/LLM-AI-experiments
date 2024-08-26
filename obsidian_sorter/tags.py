

def remove_tag(note_path, tag):
    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()

    updated_content = content.replace(f'#{tag}', '').replace(f'  - {tag}\n', '')
    
    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

def list_tags(note_path):
    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()

    tags = set()
    
    # Cerca i tag nel contenuto
    for line in content.split('\n'):
        if line.startswith('#'):
            tags.update([tag.strip() for tag in line.split() if tag.startswith('#')])

    # Cerca i tag nella sezione YAML
    yaml_section_end = content.find('---', 4)
    if content.startswith('---') and yaml_section_end != -1:
        yaml_end_index = yaml_section_end + 3
        yaml_content = content[:yaml_end_index]
        lines = yaml_content.split('\n')
        tag_line = False
        for line in lines:
            if line.strip() == 'tags:':
                tag_line = True
            elif tag_line:
                if line.strip().startswith('- '):
                    tags.add(line.strip().replace('- ', '#'))
                else:
                    tag_line = False
                    
    return list(tags)



def update_tag(note_path, old_tag, new_tag):
    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()

    updated_content = content.replace(f'#{old_tag}', f'#{new_tag}').replace(f'  - {old_tag}\n', f'  - {new_tag}\n')
    
    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

def add_tag(note_path, tag):
    tags = list_tags(note_path)
    if f'#{tag}' in tags:
        print(f"Il tag {tag} esiste già in {note_path}")
        return
    
    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verifica se c'è una sezione YAML
    yaml_section_end = content.find('---', 4)
    if content.startswith('---') and yaml_section_end != -1:
        yaml_end_index = yaml_section_end + 3
        yaml_content = content[:yaml_end_index]
        
        # Aggiungi il tag alla sezione YAML
        if 'tags:' not in yaml_content:
            yaml_content += '\ntags:\n'
        yaml_content += f'  - {tag}\n'
        
        updated_content = yaml_content + content[yaml_end_index:]
    else:
        # Aggiungi il tag alla fine del contenuto
        updated_content = content + f'\n#{tag}'

    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
