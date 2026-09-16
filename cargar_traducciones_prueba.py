"""
Carga traducciones de prueba (ingles, chino, arabe) para los primeros 20 terminos.
"""
from core.models import Termino, Idioma, TraduccionTermino


# Mapa de traducciones por termino
# Formato: 'palabra': { 'codigo_idioma': (traduccion, definicion_nativa, notas) }
TRADUCCIONES = {
    'casa': {
        'en': ('house', 'A building for people to live in.', ''),
        'zh-hans': ('房子', '供人居住的建筑物', ''),
        'ar': ('بيت', 'مبنى للسكن', ''),
    },
    'agua': {
        'en': ('water', 'Clear liquid essential for life.', ''),
        'zh-hans': ('水', '生命必需的透明液体', ''),
        'ar': ('ماء', 'سائل شفاف ضروري للحياة', ''),
    },
    'amor': {
        'en': ('love', 'Deep feeling of affection.', ''),
        'zh-hans': ('爱', '深厚的情感', ''),
        'ar': ('حب', 'شعور عميق بالمودة', ''),
    },
    'vida': {
        'en': ('life', 'State of activity of living beings.', ''),
        'zh-hans': ('生命', '生物的活动状态', ''),
        'ar': ('حياة', 'حالة نشاط الكائنات الحية', ''),
    },
    'tiempo': {
        'en': ('time', 'Magnitude that measures duration.', ''),
        'zh-hans': ('时间', '衡量持续时间的量', ''),
        'ar': ('وقت', 'مقياس المدة الزمنية', ''),
    },
    'trabajo': {
        'en': ('work', 'Physical or intellectual activity.', ''),
        'zh-hans': ('工作', '体力或智力活动', ''),
        'ar': ('عمل', 'نشاط بدني أو فكري', ''),
    },
    'familia': {
        'en': ('family', 'Group of related people.', ''),
        'zh-hans': ('家庭', '有亲属关系的人群', ''),
        'ar': ('عائلة', 'مجموعة من الأقارب', ''),
    },
    'amigo': {
        'en': ('friend', 'Person with whom one has friendship.', ''),
        'zh-hans': ('朋友', '有友谊关系的人', ''),
        'ar': ('صديق', 'شخص تربطه به صداقة', ''),
    },
    'salud': {
        'en': ('health', 'State of physical and mental well-being.', ''),
        'zh-hans': ('健康', '身体和精神健康的状态', ''),
        'ar': ('صحة', 'حالة السلامة الجسدية والنفسية', ''),
    },
    'educación': {
        'en': ('education', 'Training aimed at developing capacity.', ''),
        'zh-hans': ('教育', '旨在发展能力的培养', ''),
        'ar': ('تعليم', 'تدريب يهدف إلى تنمية القدرات', ''),
    },
    'cultura': {
        'en': ('culture', 'Set of knowledge and customs.', ''),
        'zh-hans': ('文化', '知识和习俗的集合', ''),
        'ar': ('ثقافة', 'مجموعة من المعارف والعادات', ''),
    },
    'historia': {
        'en': ('history', 'Narration of past events.', ''),
        'zh-hans': ('历史', '对过去事件的叙述', ''),
        'ar': ('تاريخ', 'سرد الأحداث الماضية', ''),
    },
    'ciencia': {
        'en': ('science', 'Systematic knowledge of reality.', ''),
        'zh-hans': ('科学', '对现实的系统知识', ''),
        'ar': ('علم', 'معرفة منهجية بالواقع', ''),
    },
    'arte': {
        'en': ('art', 'Manifestation of human creativity.', ''),
        'zh-hans': ('艺术', '人类创造力的表现', ''),
        'ar': ('فن', 'تعبير عن الإبداع البشري', ''),
    },
    'música': {
        'en': ('music', 'Art of combining sounds.', ''),
        'zh-hans': ('音乐', '组合声音的艺术', ''),
        'ar': ('موسيقى', 'فن دمج الأصوات', ''),
    },
    'libro': {
        'en': ('book', 'Set of bound sheets.', ''),
        'zh-hans': ('书', '装订成册的书页', ''),
        'ar': ('كتاب', 'مجموعة من الصفحات المجلدة', ''),
    },
    'palabra': {
        'en': ('word', 'Linguistic unit with meaning.', ''),
        'zh-hans': ('词', '具有意义的语言单位', ''),
        'ar': ('كلمة', 'وحدة لغوية ذات معنى', ''),
    },
    'lengua': {
        'en': ('language', 'System of verbal communication.', ''),
        'zh-hans': ('语言', '口头交流系统', ''),
        'ar': ('لغة', 'نظام التواصل اللفظي', ''),
    },
    'mundo': {
        'en': ('world', 'Set of all existing things.', ''),
        'zh-hans': ('世界', '所有存在事物的集合', ''),
        'ar': ('عالم', 'مجموعة كل الأشياء الموجودة', ''),
    },
    'naturaleza': {
        'en': ('nature', 'Set of natural beings.', ''),
        'zh-hans': ('自然', '自然存在物的集合', ''),
        'ar': ('طبيعة', 'مجموعة الكائنات الطبيعية', ''),
    },
}


def main():
    print('=' * 60)
    print('CARGANDO TRADUCCIONES DE PRUEBA')
    print('=' * 60)

    creadas = 0
    actualizadas = 0
    errores = 0

    for palabra, idiomas in TRADUCCIONES.items():
        try:
            termino = Termino.objects.filter(palabra__iexact=palabra).first()
            if not termino:
                print(f'  AVISO: termino "{palabra}" no existe')
                continue

            for codigo_idioma, datos in idiomas.items():
                traduccion, definicion, notas = datos
                idioma = Idioma.objects.filter(codigo=codigo_idioma).first()
                if not idioma:
                    print(f'  AVISO: idioma "{codigo_idioma}" no existe')
                    continue

                trad, created = TraduccionTermino.objects.get_or_create(
                    termino=termino,
                    idioma=idioma,
                    defaults={
                        'traduccion': traduccion,
                        'definicion_nativa': definicion,
                        'notas': notas,
                        'nivel_correspondencia': 'exacta',
                    }
                )
                if created:
                    creadas += 1
                else:
                    trad.traduccion = traduccion
                    trad.definicion_nativa = definicion
                    trad.save()
                    actualizadas += 1

        except Exception as e:
            errores += 1
            print(f'  ERROR en "{palabra}": {e}')

    print()
    print('=' * 60)
    print('RESUMEN')
    print('=' * 60)
    print(f'Traducciones creadas:      {creadas}')
    print(f'Traducciones actualizadas: {actualizadas}')
    print(f'Errores:                   {errores}')
    print(f'Total en BD:               {TraduccionTermino.objects.count()}')
    print('=' * 60)


main()