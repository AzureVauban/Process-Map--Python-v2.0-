#pragma once
#include <iostream>
#include <string>
#include <cmath>
#include <vector>
#include <fstream>
#include <sstream>
#include <algorithm>
bool isdigit_check(const std::string basestring = "")
{
    bool isdigit = false;
    for (const auto &character : basestring)
    {
        isdigit = (int)character <= 57 and (int) character >= 48;
        if (not isdigit)
        {
            break;
        }
    }
    return isdigit;
}
int integer_input()
{
    int returnint = 0;
    std::string userinpput = "";
    std::stringstream buffer;
    do
    {
        std::getline(std::cin, userinpput);
        std::remove(userinpput.begin(), userinpput.end(), ' ');
        if (not isdigit_check(userinpput))
        {
            std::cout << "Please type in an interger" << std::endl;
        }
    } while (not isdigit_check(userinpput));
    buffer << userinpput;
    buffer >> returnint;
    return returnint;
}
namespace NodeUtility
{

    struct Node
    {
        //! using namespace NodeUtility;
        std::string ingredient;
        int amountonhand = 0,
            amountneeded = 0,
            amountmadepercraft = 0,
            amountresulted = 0,
            generation = 0;
        Node *parent;
        std::vector<Node *> children;
        Node(std::string name = "", Node *par = nullptr, int amount_on_hand = 0, int amount_parent_madepercraft = 1, int amount_needed = 1, const bool promptdiffers = false)
        {
            generation = 0;
            ingredient = name;
            parent = par;
            if (parent)
            {
                generation = parent->generation + 1;
                parent->children.emplace_back(this);
            }
            amountonhand = amount_on_hand;
            amountmadepercraft = amount_parent_madepercraft;
            amountneeded = amount_needed;
            if (parent and promptdiffers)
            {
                std::cout << "What is the amount of " << parent->ingredient << " you create each time you craft it? " << std::endl;
                amountmadepercraft = integer_input();
            }
            if (parent)
            {
                std::cout << "What is the amount of " << ingredient << " you need to craft " << parent->ingredient << " 1 time?" << std::endl;
                amountneeded = integer_input();
            }
        }
        ~Node()
        {
            std::cout << "DEALLOCATING " << ingredient << " : " << this << std::endl;
        }
    };
    // set the amount on hand to the desired amount/assertvalue
    int setassertvalues(Node *object, int desiredamount = 0)
    {
        // figure out how much the assert should be, the long way
        object->amountonhand = desiredamount * std::pow(double(object->amountmadepercraft) / double(object->amountneeded), -1.00);
        // iterate through the children subnodes
        for (auto child : object->children)
        {
            setassertvalues(child, object->amountonhand);
        }
        std::cout << "FINISH SETTING ASSERT VALUE FOR " << object->ingredient << std::endl;
        return object->amountonhand;
    }
}

void massdelete(NodeUtility::Node *obj)
{
    for (auto child : obj->children)
    {
        massdelete(child);
    }
    delete obj;
}
// functions for writting and creating the unit test module
namespace format
{
    enum formattype
    {
        defaulttype = 0,
        docstring = 1,
        classname = 2,
        method = 3,
        instance_declaration = 4
    };
    // todo add functions for formatting here
    std::string formatstring(const std::string basestring, const formattype type = defaulttype)
    {
        std::string returnstring = basestring;
        switch (type)
        {
        case docstring: // return no spaces, replace spaces with underscore
            for (auto &character : returnstring)
            {
                if (character == ' ')
                {
                    character = '_';
                }
            }
            break;
        case classname: // return no spaces and all caps
            std::remove(returnstring.begin(), returnstring.end(), ' ');
            for (auto &character : returnstring)
            {
                character = std::toupper(character);
            }
            break;
        case instance_declaration:
            for (auto &character : returnstring)
            {
                if (character == ' ')
                {
                    character = '_';
                }
            }
        default: // return no spaces, replace spaces with underscore
            for (auto &character : returnstring)
            {
                if (character == ' ')
                {
                    character = '_';
                }
            }
        }
        return returnstring;
    }
    // function for appending numbers to ingredient names to make ingredient names unique

}
namespace write_unittest_module
{
    using namespace NodeUtility;
    const std::string docstringprefix = "\"\"\"";
    // create functions for writing onto ostream object here
    void tabbing(std::ofstream &module, const int tablevel = 1)
    {
        for (int i = 0; i < tablevel; i++)
        {
            module << "\t";
        }
    }
    namespace docstring
    {

        void module(std::ofstream &module)
        {
            module << write_unittest_module::docstringprefix << "AUTO GENERATED UNIT TEST" << std::endl
                   << write_unittest_module::docstringprefix << std::endl;

            module << "import unittest" << std::endl
                   << std::endl;
            module << "from main import Node, reversearithmetic" << std::endl;
        }
        void classdoc(std::ofstream &module)
        {
            tabbing(module, 1);
            module << docstringprefix << "tentative test class, add additional comments here:" << std::endl;
            tabbing(module, 1);
            module << docstringprefix << std::endl;
        }
        void method(std::ofstream &module, const Node *object)
        {
            // docstring for test method
            tabbing(module, 2);
            module << docstringprefix << "assert that " << object->ingredient << " is equal to " << object->amountonhand << std::endl;
            tabbing(module, 2);
            module << docstringprefix;
            module << std::endl
                   << std::endl;
        }
    }
    void declaration(std::ofstream &module, const Node *object)
    {
        std::string parentstring = "None";
        if (object->parent)
        {
            parentstring = format::formatstring(object->parent->ingredient, format::instance_declaration);
        }
        module << format::formatstring(object->ingredient, format::instance_declaration) << ": Node = Node('" << object->ingredient << "', " << parentstring << ", " << 0 << ", " << object->amountmadepercraft << ", " << object->amountneeded << ")" << std::endl;
    }
    void method(std::ofstream &module, const Node *object)
    {
        tabbing(module, 1);
        module << "def test_" << format::formatstring(object->ingredient, format::method) << "(self): # pylint:disable=C0103" << std::endl;
        write_unittest_module::docstring::method(module, object);
        tabbing(module, 2);
        module << "self.assertEqual(" << format::formatstring(object->ingredient, format::instance_declaration) << ".amountonhand," << object->amountonhand << ")" << std::endl;
    }
    void tree_declaration(std::ofstream &module, const Node *object)
    {
        write_unittest_module::declaration(module, object);
        for (auto miniobject : object->children)
        {
            tree_declaration(module, miniobject);
        }
    }
    void tree_method(std::ofstream &module, const Node *object)
    {
        write_unittest_module::method(module, object);
        module << std::endl;
        for (const auto miniobject : object->children)
        {
            tree_method(module, miniobject);
        }
    }
    void createclass(std::ofstream &module, Node *object)
    {
        Node *temp = object;
        while (temp->parent)
        {
            temp = temp->parent;
        }
        module << "class " << format::formatstring(temp->ingredient, format::classname) << "_unittest"
               << "(unittest.TestCase): # pylint:disable=C0103" << std::endl;
        docstring::classdoc(module);
        module << std::endl;
    }
}
namespace write_CSV_file
{
    using namespace NodeUtility;
    // functions for writing to a CSV file
    void writedata(const Node *node, std::ostream &CSVfile)
    {
        /* write contents in this format
        ingredient,parent_ingredient,amount_on_hand,amount_made_per_craft,amount_needed,generation
        */
        std::string parentingredient = "None";
        if (node->parent)
        {
            parentingredient = format::formatstring(node->parent->ingredient, format::docstring);
        }
        if (not node->parent)
        {
            CSVfile << "Ingredient;ParentIngredient;AmountonHand;AmountMadePerCraft;AmountNeeded;Generation" << std::endl;
        }
        CSVfile << format::formatstring(node->ingredient, format::docstring) << ";" << parentingredient << ";";
        CSVfile << node->amountonhand << ";" << node->amountneeded << ";" << node->amountmadepercraft << ";" << node->generation << std::endl;
        for (const auto childnode : node->children)
        {
            writedata(childnode, CSVfile);
        }
    }
}
