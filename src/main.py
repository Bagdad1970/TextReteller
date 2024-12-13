from lib.EntityFinder import EntityFinder
from lib.SemanticAnalyzer import SemanticAnalyzer
from lib.FileManager import FileManager
from lib.RelationGraph import RelationGraph
from lib.TextCleaner import TextCleaner
from lib.WeekEntityFinder import WeekEntityFinder


def main():
    text = ('Филадельфия, где родился Фрэнк Алджернон Каупервуд, насчитывала тогда '
            'более двухсот пятидесяти тысяч жителей Домодедово. Филадельфия этот изобиловал красивыми парками, '
            'величественными зданиями и памятниками старины.')

    text = ('На улице стояла прохладная осенняя погода, и в воздухе ощущался запах дождя. '
            'Прохожие торопливо шагали по мокрым тротуарам, прячась под разноцветными зонтиками. '
            'Вдалеке слышался гул автомобилей, который смешивался с шуршанием опавших листьев под ногами. '
            'В одном из окон виднелся тусклый свет лампы, за которой мелькала тень человека. '
            'На лавочке в парке сидел пожилой мужчина, задумчиво глядя в сторону серого неба. '
            'Ветер время от времени усиливался, поднимая в воздух мелкий мусор и легкие листья. '
            'Над головой кружили птицы, будто решая, куда отправиться дальше. '
            'Из соседнего кафе доносился аромат свежеиспеченного хлеба и бодрящий запах кофе. '
            'Люди сновали туда-сюда, каждый с собственными заботами и мыслями. '
            'День постепенно клонился к закату, окрашивая небо мягкими оттенками розового и оранжевого.')

    text = """Планета обладала густой неспокойной атмосферой, похожей на оранжевый океан. 
    Движение газа отражалось чрезвычайно сложным, непрерывно меняющимся узором линий. 
    Изображение планеты продолжало расти, пока не заслонило собой всю Вселенную; наблюдателей поглотил ее оранжевый газообразный океан. 
    Зонд провел их сквозь плотные облака туда, где туман был не столь густым, что позволило увидеть формы жизни на планете. 
    В верхних слоях атмосферы плавала стая животных эллипсоидной формы. 
    Их тела покрывали очень приятные на вид калейдоскопические узоры, мгновенно менявшиеся с набора полос на точки и так далее; вероятно, это был своеобразный визуальный язык. 
    Каждый эллипсоид имел длинный хвост, на кончике которого то и дело возникала яркая вспышка, пробегавшая по всей длине хвоста и заполнявшая баллон рассеянным свечением."""

    #text = 'Изображение планеты продолжало расти, пока не заслонило собой всю Вселенную; наблюдателей поглотил ее оранжевый газообразный океан. '

    #text = "Каждый эллипсоид имел длинный хвост, на кончике которого то и дело возникала яркая вспышка, пробегавшая по всей длине хвоста и заполнявшая баллон рассеянным свечением."

    #text = 'Планета обладала густой неспокойной атмосферой, похожей на оранжевый океан. Кошка на столе ела мясо. '

    file_manager = FileManager()

    entity_finder = EntityFinder(text)
    entity_dict = entity_finder.find_entities()

    semantic_analyzer = SemanticAnalyzer(text, entity_dict)
    semantic_analyzer.importance_of_entities()
    couples_of_vertex = semantic_analyzer.relation_of_entities()

    graph = RelationGraph(couples_of_vertex)
    graph.traverse_and_update_depth()
    weighted_vertexes = graph.get_weighted_vertexes()

    entity_dict.attach_entity_mains(weighted_vertexes)

    week_entity_finder = WeekEntityFinder(entity_dict)
    week_entities = week_entity_finder.find_week_entities(0.7)

    text_cleaner = TextCleaner(text, week_entities)
    text_cleaner.delete_words_by_indexes()

if __name__ == '__main__':
    main()